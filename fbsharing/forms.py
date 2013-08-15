from django import forms
from fbsharing.models import fbDataRequest, Campaign


class dataForm(forms.ModelForm):
	class Meta:
		model = fbDataRequest
		fields = ("url",)


class CampaignForm(forms.ModelForm):
	class Meta:
		model = Campaign
		fields = ("url", "end_date", "current")