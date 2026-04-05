from datetime import datetime, timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils import timezone

from .models import Pomodoro, Tag, UserSettings, Rewards, Statistics, get_period_start


# Fixed "now" = Wednesday 2026-04-15 12:00 UTC
FIXED_NOW = timezone.make_aware(datetime(2026, 4, 15, 12, 0, 0))

TEST_SETTINGS = dict(
    CSRF_COOKIE_SECURE=False,
    SESSION_COOKIE_SECURE=False,
    SECURE_SSL_REDIRECT=False,
    CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}},
)


def create_test_user(username, password="testpass123!"):
    user = User.objects.create_user(username=username, password=password)
    UserSettings.objects.create(user=user)
    Rewards.objects.create(user=user)
    return user


def make_pomodoro(user, tag, dt):
    return Pomodoro.objects.create(user=user, tag=tag, datetime=dt)


# ── Timestamps relative to FIXED_NOW (2026-04-15 Wed 12:00 UTC) ──
# Week start = Mon 2026-04-13 00:00
# Month start = 2026-04-01 00:00
# Year start = 2026-01-01 00:00

TS_WEEK_1 = timezone.make_aware(datetime(2026, 4, 15, 10, 0))   # today
TS_WEEK_2 = timezone.make_aware(datetime(2026, 4, 14, 10, 0))   # yesterday (Tue)
TS_MONTH_1 = timezone.make_aware(datetime(2026, 4, 5, 10, 0))   # this month, not this week
TS_MONTH_2 = timezone.make_aware(datetime(2026, 4, 2, 10, 0))   # this month, not this week
TS_YEAR_1 = timezone.make_aware(datetime(2026, 2, 15, 10, 0))   # this year, not this month
TS_YEAR_2 = timezone.make_aware(datetime(2026, 1, 10, 10, 0))   # this year, not this month
TS_OLD_1 = timezone.make_aware(datetime(2025, 6, 15, 10, 0))    # older than a year
TS_OLD_2 = timezone.make_aware(datetime(2025, 1, 10, 10, 0))    # older than a year


# ─────────────────────────────────────────────────────────────────
# 1. Unit tests for get_period_start()
# ─────────────────────────────────────────────────────────────────

class TestGetPeriodStart(TestCase):

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_week_returns_monday_midnight(self, _mock):
        result = get_period_start('week')
        self.assertEqual(result.weekday(), 0)  # Monday
        self.assertEqual(result.hour, 0)
        self.assertEqual(result.minute, 0)
        self.assertEqual(result.second, 0)
        self.assertEqual(result.date(), datetime(2026, 4, 13).date())

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_month_returns_first_of_month(self, _mock):
        result = get_period_start('month')
        self.assertEqual(result.day, 1)
        self.assertEqual(result.month, 4)
        self.assertEqual(result.hour, 0)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_year_returns_jan_first(self, _mock):
        result = get_period_start('year')
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        self.assertEqual(result.year, 2026)

    def test_all_returns_none(self):
        self.assertIsNone(get_period_start('all'))

    def test_invalid_returns_none(self):
        self.assertIsNone(get_period_start('invalid'))

    def test_empty_returns_none(self):
        self.assertIsNone(get_period_start(''))


# ─────────────────────────────────────────────────────────────────
# 2. Statistics with filtered querysets
# ─────────────────────────────────────────────────────────────────

@override_settings(**TEST_SETTINGS)
class TestStatisticsWithFiltering(TestCase):

    def setUp(self):
        self.user = create_test_user('statuser')
        self.tag_work = Tag.objects.create(tag='stat_work')
        self.tag_study = Tag.objects.create(tag='stat_study')
        # 3 work this week, 2 study older
        make_pomodoro(self.user, self.tag_work, TS_WEEK_1)
        make_pomodoro(self.user, self.tag_work, TS_WEEK_2)
        make_pomodoro(self.user, self.tag_work, TS_MONTH_1)
        make_pomodoro(self.user, self.tag_study, TS_YEAR_1)
        make_pomodoro(self.user, self.tag_study, TS_OLD_1)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_average_all(self, _m):
        avg = Statistics.getAveragePomodoros(self.user)
        self.assertGreater(avg, 0)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_average_filtered(self, _m):
        week_qs = self.user.pomodoros.filter(datetime__gte=TS_WEEK_2.replace(hour=0))
        avg_week = Statistics.getAveragePomodoros(self.user, pomodoros=week_qs)
        avg_all = Statistics.getAveragePomodoros(self.user)
        self.assertNotEqual(avg_week, avg_all)

    def test_average_empty(self):
        empty_qs = self.user.pomodoros.none()
        self.assertEqual(Statistics.getAveragePomodoros(self.user, pomodoros=empty_qs), 0)

    def test_aggregate_all(self):
        result = Statistics.aggregatePomodorosByTag(self.user)
        self.assertIn('stat_work', result)
        self.assertIn('stat_study', result)
        self.assertEqual(result['stat_work'], 3)
        self.assertEqual(result['stat_study'], 2)

    def test_aggregate_filtered(self):
        week_qs = self.user.pomodoros.filter(datetime__gte=TS_WEEK_2.replace(hour=0))
        result = Statistics.aggregatePomodorosByTag(self.user, pomodoros=week_qs)
        self.assertIn('stat_work', result)
        self.assertNotIn('stat_study', result)

    def test_aggregate_empty(self):
        empty_qs = self.user.pomodoros.none()
        self.assertEqual(Statistics.aggregatePomodorosByTag(self.user, pomodoros=empty_qs), {})

    def test_aggregate_sorted_descending(self):
        result = Statistics.aggregatePomodorosByTag(self.user)
        values = list(result.values())
        self.assertEqual(values, sorted(values, reverse=True))


# ─────────────────────────────────────────────────────────────────
# 3. Pomodoros list view filtering
# ─────────────────────────────────────────────────────────────────

@override_settings(**TEST_SETTINGS)
class TestPomodorosListFiltering(TestCase):

    def setUp(self):
        self.user = create_test_user('pomouser')
        self.tag = Tag.objects.create(tag='pomo_work')
        # 2 this week, 2 month-only, 2 year-only, 2 old
        make_pomodoro(self.user, self.tag, TS_WEEK_1)
        make_pomodoro(self.user, self.tag, TS_WEEK_2)
        make_pomodoro(self.user, self.tag, TS_MONTH_1)
        make_pomodoro(self.user, self.tag, TS_MONTH_2)
        make_pomodoro(self.user, self.tag, TS_YEAR_1)
        make_pomodoro(self.user, self.tag, TS_YEAR_2)
        make_pomodoro(self.user, self.tag, TS_OLD_1)
        make_pomodoro(self.user, self.tag, TS_OLD_2)
        self.client.login(username='pomouser', password='testpass123!')

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get('/pomodoros')
        self.assertEqual(resp.status_code, 302)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_default_period_all(self, _m):
        resp = self.client.get('/pomodoros')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['current_period'], 'all')
        self.assertEqual(resp.context['page_obj'].paginator.count, 8)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_filter_week(self, _m):
        resp = self.client.get('/pomodoros?period=week')
        self.assertEqual(resp.context['current_period'], 'week')
        self.assertEqual(resp.context['page_obj'].paginator.count, 2)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_filter_month(self, _m):
        resp = self.client.get('/pomodoros?period=month')
        self.assertEqual(resp.context['current_period'], 'month')
        self.assertEqual(resp.context['page_obj'].paginator.count, 4)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_filter_year(self, _m):
        resp = self.client.get('/pomodoros?period=year')
        self.assertEqual(resp.context['current_period'], 'year')
        self.assertEqual(resp.context['page_obj'].paginator.count, 6)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_filter_all_explicit(self, _m):
        resp = self.client.get('/pomodoros?period=all')
        self.assertEqual(resp.context['page_obj'].paginator.count, 8)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_active_class_on_month(self, _m):
        resp = self.client.get('/pomodoros?period=month')
        content = resp.content.decode()
        self.assertIn('href="?period=month" class="active"', content)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_inactive_buttons_no_active(self, _m):
        resp = self.client.get('/pomodoros?period=month')
        content = resp.content.decode()
        self.assertNotIn('href="?period=week" class="active"', content)
        self.assertNotIn('href="?period=year" class="active"', content)
        self.assertNotIn('href="?period=all" class="active"', content)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_pagination_preserves_period(self, _m):
        # Create 55 pomodoros this week to trigger pagination (50 per page)
        tag = self.tag
        for i in range(55):
            make_pomodoro(self.user, tag, TS_WEEK_1 - timedelta(minutes=i))
        resp = self.client.get('/pomodoros?period=week')
        content = resp.content.decode()
        self.assertIn('period=week&page=2', content)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_pagination_page2_with_period(self, _m):
        for i in range(55):
            make_pomodoro(self.user, self.tag, TS_WEEK_1 - timedelta(minutes=i))
        resp = self.client.get('/pomodoros?period=week&page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['current_period'], 'week')

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_empty_period(self, _m):
        # Create a user with no pomodoros this week
        user2 = create_test_user('emptyuser')
        tag2 = Tag.objects.create(tag='empty_tag')
        make_pomodoro(user2, tag2, TS_OLD_1)
        self.client.login(username='emptyuser', password='testpass123!')
        resp = self.client.get('/pomodoros?period=week')
        content = resp.content.decode()
        self.assertIn('No pomodoros to show', content)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_invalid_period_treated_as_all(self, _m):
        resp = self.client.get('/pomodoros?period=garbage')
        self.assertEqual(resp.context['page_obj'].paginator.count, 8)


# ─────────────────────────────────────────────────────────────────
# 4. Own profile filtering
# ─────────────────────────────────────────────────────────────────

@override_settings(**TEST_SETTINGS)
class TestOwnProfileFiltering(TestCase):

    def setUp(self):
        self.user = create_test_user('profileuser')
        self.tag_work = Tag.objects.create(tag='prof_work')
        self.tag_study = Tag.objects.create(tag='prof_study')
        # 3 work this week, 1 study this month, 1 work old
        make_pomodoro(self.user, self.tag_work, TS_WEEK_1)
        make_pomodoro(self.user, self.tag_work, TS_WEEK_2)
        make_pomodoro(self.user, self.tag_work, TS_MONTH_1)
        make_pomodoro(self.user, self.tag_study, TS_MONTH_2)
        make_pomodoro(self.user, self.tag_work, TS_OLD_1)
        self.client.login(username='profileuser', password='testpass123!')

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_default_period_all(self, _m):
        resp = self.client.get('/profileuser/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['current_period'], 'all')
        self.assertTrue(resp.context['display'])

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_filter_week_tag_counts(self, _m):
        resp = self.client.get('/profileuser/?period=week')
        self.assertEqual(resp.context['current_period'], 'week')
        # Only work tag this week (2 pomos)
        tags = {item[0]: item[1] for item in resp.context['page_obj']}
        self.assertIn('prof_work', tags)
        self.assertNotIn('prof_study', tags)
        self.assertEqual(tags['prof_work'], 2)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_filter_month_tag_counts(self, _m):
        resp = self.client.get('/profileuser/?period=month')
        tags = {item[0]: item[1] for item in resp.context['page_obj']}
        self.assertEqual(tags['prof_work'], 3)  # week(2) + month(1)
        self.assertEqual(tags['prof_study'], 1)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_average_changes_with_period(self, _m):
        resp_all = self.client.get('/profileuser/?period=all')
        resp_week = self.client.get('/profileuser/?period=week')
        self.assertNotEqual(resp_all.context['averagePomos'], resp_week.context['averagePomos'])

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_active_filter_class(self, _m):
        resp = self.client.get('/profileuser/?period=month')
        content = resp.content.decode()
        self.assertIn('href="?period=month" class="active"', content)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_empty_period(self, _m):
        user2 = create_test_user('emptyprofile')
        tag = Tag.objects.create(tag='ep_tag')
        make_pomodoro(user2, tag, TS_OLD_1)
        self.client.login(username='emptyprofile', password='testpass123!')
        resp = self.client.get('/emptyprofile/?period=week')
        self.assertEqual(resp.context['averagePomos'], 0)
        self.assertEqual(len(resp.context['page_obj'].object_list), 0)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_has_settings_form(self, _m):
        resp = self.client.get('/profileuser/')
        self.assertIn('form', resp.context)
        self.assertTrue(resp.context['display'])

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_pagination_preserves_period(self, _m):
        # Create 15 unique tags with pomodoros to trigger pagination (13 per page)
        for i in range(15):
            t = Tag.objects.create(tag=f'pag_tag_{i}')
            make_pomodoro(self.user, t, TS_WEEK_1 - timedelta(hours=i))
        resp = self.client.get('/profileuser/?period=all')
        content = resp.content.decode()
        self.assertIn('period=all&page=', content)


# ─────────────────────────────────────────────────────────────────
# 5. Public profile filtering
# ─────────────────────────────────────────────────────────────────

@override_settings(**TEST_SETTINGS)
class TestPublicProfileFiltering(TestCase):

    def setUp(self):
        self.public_user = create_test_user('publicuser')
        self.tag = Tag.objects.create(tag='pub_work')
        make_pomodoro(self.public_user, self.tag, TS_WEEK_1)
        make_pomodoro(self.public_user, self.tag, TS_OLD_1)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_anonymous_default_all(self, _m):
        resp = self.client.get('/publicuser/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['current_period'], 'all')

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_anonymous_filter_week(self, _m):
        resp = self.client.get('/publicuser/?period=week')
        self.assertEqual(resp.context['current_period'], 'week')

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_different_user_sees_public_view(self, _m):
        viewer = create_test_user('viewer')
        self.client.login(username='viewer', password='testpass123!')
        resp = self.client.get('/publicuser/?period=month')
        self.assertEqual(resp.context['current_period'], 'month')
        self.assertNotIn('display', resp.context)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_has_chart_period_filter_div(self, _m):
        resp = self.client.get('/publicuser/')
        content = resp.content.decode()
        self.assertIn('id="chart-period-filter"', content)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_uses_span_tags(self, _m):
        resp = self.client.get('/publicuser/')
        content = resp.content.decode()
        self.assertIn('<span data-period="week">Week</span>', content)
        self.assertIn('<span data-period="month">Month</span>', content)
        self.assertIn('<span data-period="year">Year</span>', content)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_no_form_in_context(self, _m):
        resp = self.client.get('/publicuser/')
        self.assertNotIn('form', resp.context)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_no_page_obj_in_context(self, _m):
        resp = self.client.get('/publicuser/')
        self.assertNotIn('page_obj', resp.context)

    def test_nonexistent_user_404(self):
        resp = self.client.get('/nonexistent/')
        self.assertEqual(resp.status_code, 404)

    @patch('app.models.timezone.now', return_value=FIXED_NOW)
    def test_empty_period(self, _m):
        user2 = create_test_user('nopomo')
        resp = self.client.get('/nopomo/?period=week')
        self.assertEqual(resp.context['averagePomos'], 0)


# ─────────────────────────────────────────────────────────────────
# 6. Charts page
# ─────────────────────────────────────────────────────────────────

@override_settings(**TEST_SETTINGS)
class TestChartsPage(TestCase):

    def setUp(self):
        self.user = create_test_user('chartuser')
        self.client.login(username='chartuser', password='testpass123!')

    def test_login_required(self):
        self.client.logout()
        resp = self.client.get('/charts')
        self.assertEqual(resp.status_code, 302)

    def test_page_loads(self):
        resp = self.client.get('/charts')
        self.assertEqual(resp.status_code, 200)

    def test_has_period_filter_div(self):
        resp = self.client.get('/charts')
        content = resp.content.decode()
        self.assertIn('id="chart-period-filter"', content)

    def test_has_all_four_period_spans(self):
        resp = self.client.get('/charts')
        content = resp.content.decode()
        self.assertIn('data-period="week"', content)
        self.assertIn('data-period="month"', content)
        self.assertIn('data-period="year"', content)
        self.assertIn('data-period="all"', content)

    def test_all_is_default_active(self):
        resp = self.client.get('/charts')
        content = resp.content.decode()
        self.assertIn('data-period="all" class="active"', content)

    def test_has_chart_containers(self):
        resp = self.client.get('/charts')
        content = resp.content.decode()
        self.assertIn('id="pie-chart"', content)
        self.assertIn('id="bar-chart-first"', content)
        self.assertIn('id="bar-chart-second"', content)
