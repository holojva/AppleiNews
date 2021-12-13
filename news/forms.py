from django import forms

from .models import News

# class NewsForm(forms.Form) :
#     article = forms.CharField()
#     body = forms.CharField(widget=forms.Textarea)

class NewsModelForm(forms.ModelForm) :
    class Meta:
        model = News
        fields = [
            "article",
            "body"
        ]
    
    def clean_article(self) :
        data = self.cleaned_data.get("article")
        if len(data) < 5:
            raise forms.ValidationError("Article is not long enough")
        return data