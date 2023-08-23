import { theme } from './user_settings.js';

// Fetch the leaderboard data
const data = fetch('/api/leaderboard').
  then((response) => {
    if (response.status !== 200) return null;
    return response.json();
  }
).then((data) => {
  return data;
});
// Add event listener to the period buttons
const radioInputs = document.querySelectorAll('input[type="radio"][name="plan"]');
radioInputs.forEach(radioInput => {
    radioInput.addEventListener('change', function() {
        if (this.checked) {
            let selectedPeriod = this.id;
            displayLeaderboard(selectedPeriod, data);

        }
    });
});


function displayLeaderboard(selectedPeriod, data) {
  deleteLeaderboard();
  data.then((data) => {
    data = orderData(data, selectedPeriod);
    for (const user of Object.keys(data)) {
      const delay = Object.keys(data).indexOf(user) * 0.1;
      displayItemDelay(user, delay, selectedPeriod, data);
      }
    }
  );
}


function orderData(data, selectedPeriod) {
  const orderedData = {};
  const users = Object.keys(data);
  users.sort((a, b) => {
    const aCount = getCountPeriod(data[a]['pomos'], selectedPeriod);
    const bCount = getCountPeriod(data[b]['pomos'], selectedPeriod);
    return bCount - aCount;
  });
  for (const user of users) {
    orderedData[user] = data[user];
  }
  return orderedData;
}


function displayItemDelay(user, delay, selectedPeriod, data) {
  setTimeout(() => {
    const rewards = data[user]['rewards'];
    const image = data[user]['image'];
    const count = getCountPeriod(data[user]['pomos'], selectedPeriod);
    if (count > 0) {
      const userLeaderboard = document.createElement('li');
      userLeaderboard.classList.add('user-leaderboard');

      const leftContainer = document.createElement('div');
      leftContainer.classList.add('left');

      const profileImg = document.createElement('img');
      profileImg.src = `https://crpjolyxva.cloudimg.io/pomotracker.s3.eu-central-1.amazonaws.com/${image}`;
      profileImg.alt = 'profile picture';
      profileImg.classList.add('user-profile-img');
      leftContainer.appendChild(profileImg);

      const usernameLink = document.createElement('a');
      usernameLink.href = `/${user}/`;
      usernameLink.textContent = user;
      const usernameParagraph = document.createElement('p');
      usernameParagraph.appendChild(usernameLink);
      leftContainer.appendChild(usernameParagraph);

      const rewardsContainer = document.createElement('div');
      rewardsContainer.classList.add('rewards-container');
      if (rewards.gold) {
        const goldSpan = document.createElement('span');
        goldSpan.classList.add('rewards');
        goldSpan.textContent = `🥇${rewards.gold}`;
        rewardsContainer.appendChild(goldSpan);
      }
      if (rewards.silver) {
        const silverSpan = document.createElement('span');
        silverSpan.classList.add('rewards');
        silverSpan.textContent = `🥈${rewards.silver}`;
        rewardsContainer.appendChild(silverSpan);
      }
      if (rewards.bronze) {
        const bronzeSpan = document.createElement('span');
        bronzeSpan.classList.add('rewards');
        bronzeSpan.textContent = `🥉${rewards.bronze}`;
        rewardsContainer.appendChild(bronzeSpan);
      }
      leftContainer.appendChild(rewardsContainer);

      userLeaderboard.appendChild(leftContainer);

      const rightParagraph = document.createElement('p');
      rightParagraph.classList.add('right');
      rightParagraph.textContent = count;
      userLeaderboard.appendChild(rightParagraph);

      // Append the created elements to the desired container on your page
      // For example:
      const leaderboardContainer = document.querySelector('.leaderboard-user-container');
      leaderboardContainer.appendChild(userLeaderboard);

      // Set a delay to animate the leaderboard
      setTimeout(() => {
        userLeaderboard.style.opacity = 1;
        userLeaderboard.style.transform = 'translateY(0)';
      }, 100);
    }
  }, delay * 1000);
}


function deleteLeaderboard() {
  const leaderboardContainer = document.querySelector('.leaderboard-user-container');
  while (leaderboardContainer.firstChild) {
    leaderboardContainer.removeChild(leaderboardContainer.firstChild);
  }
}


function getCountPeriod(pomodoros, period) {
  const currentDate = new Date();
  const today = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate());

  const startDate = new Date(today); // Default to today
  if (period === 'week') {
    // Calculate the day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
    const dayOfWeek = currentDate.getDay();
    // Calculate the number of days to subtract to get to the start of the week (Monday)
    const daysToSubtract = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    // Subtract the days to get to the start of the week
    startDate.setDate(currentDate.getDate() - daysToSubtract);
  } else if (period === 'month') {
    startDate.setDate(1); // Start of the month
  } else if (period === 'year') {
    startDate.setMonth(0, 1); // Start of the year
  } else if (period === 'total') {
    startDate.setFullYear(2020, 1, 1); // Start of the project
  }

  const endDate = new Date(today);

  endDate.setDate(today.getDate() + 1);

  let totalPomodoros = 0;
  for (const date in pomodoros) {
    if (pomodoros.hasOwnProperty(date)) {
      const currentDate = new Date(date);
      if (currentDate >= startDate && currentDate <= endDate) {
        totalPomodoros += pomodoros[date];
      }
    }
  }
  return totalPomodoros;
}

// Set the default period to month when the page loads
displayLeaderboard('month', data);