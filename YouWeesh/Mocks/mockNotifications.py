# Send to single device.
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AIzaSyCmXqLvUggroOQvuCFObVTdo7KnVffqzeo")

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "csv4GAoEDEw:APA91bGK8tE7X1ezvDVL1QPR43DDuHpPHuazOzE_k3ufXE45KWAZlkE3eidf-lP2duYW1jIJq-LISXHWE0PTLxtW7hj-MJdVDIKtGH_g3V0cOp_MRTNSFJAKgz55UXQMeD0xGuCcw9bq"
message_title = "From Backend"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

# Send to multiple devices by passing a list of ids.
'''
registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
message_title = "Uber update"
message_body = "Hope you're having fun this weekend, don't forget to check today's news"
result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
'''
print result