from django.db import models

#to give unique id to each request
import uuid

#model to see the request log
class RequestLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    request_body = models.JSONField()
    response_body = models.JSONField(null = True, blank  = True)

    #null for database allowance to accept null values of response
    #blank for validation with empty values

    latency_ms = models.JSONField(null = True, blank= True)
    status = models.CharField(max_length=20, default="pending")


    def __str__(self):
        return f"{self.id} - {self.created_at} - {self.status}"
    

