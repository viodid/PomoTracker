"""Helper functions for the view's app"""

import os
import boto3

def saveSettings(form, user):
    """Save user settings to the database"""
    settings = user.settings
    if form['image']:
        #delete_previous_image_s3(form['image'])
        upload_image_s3(form['image'])
        settings.image = form['image'].name
    if form['shortBreak']:
        settings.shortBreak = int(form['shortBreak'])
    if form['longBreak']:
        settings.longBreak = int(form['longBreak'])
    if form['theme']:
        settings.theme = form['theme']
        if form['theme'] == 'forest':
            settings.focusColor = '#EAE7B1'
        elif form['theme'] == 'aquamarine':
            settings.focusColor = '#6BAAAA'
        elif form['theme'] == 'default' or form['theme'] == 'white':
            settings.focusColor = '#f1c232'
        elif form['theme'] == 'garnet':
            settings.focusColor = '#9a1b18'
        elif form['theme'] == 'coral':
            settings.focusColor = '#FAD6A5'
    if form['startSound']:
        settings.startSound = form['startSound']
    if form['stopSound']:
        settings.stopSound = form['stopSound']
    if form['timezone']:
        settings.timezone = form['timezone']
    settings.save()


def delete_previous_image_s3(image):
    """Delete previous image from AWS S3"""
    client = connect_s3()
    client.delete_object(
        Bucket=os.environ.get('AWS_STORAGE_BUCKET_NAME'),
        Key=image
    )

def upload_image_s3(image):
    """Upload image to AWS S3"""
    client = connect_s3()
    client.upload_fileobj(
        image,
        os.environ.get('AWS_STORAGE_BUCKET_NAME'),
        image.name
    )
    return image.name

def connect_s3():
    """Connect to AWS S3"""
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
