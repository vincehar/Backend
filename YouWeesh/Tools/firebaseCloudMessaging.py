from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAArhD75Ug:APA91bHNDxUca0Z4LyHdg8z5R06urT86Ud0RdQ4kqlDeDOE-qqg7ICRP9QoRwmlxVxpaOigBlnwB865-Dgb3QNtGKHnHDRVa-yC4EvvqGUir2TcLWMwsGXW-iI_0Q8AQwwifx-sURmmL")

# OR initialize with proxies

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

#registration_id = "<device registration_id>"
message_title = "Uber update"
message_body = "Hi john, your customized news for today is ready"
result = push_service.notify_single_device( message_title=message_title, message_body=message_body)
push_service.notify_topic_subscribers()
print result
'''
# Send to multiple devices by passing a list of ids.
registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
message_title = "Uber update"
message_body = "Hope you're having fun this weekend, don't forget to check today's news"
result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

print result'''