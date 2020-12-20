from django.forms import ModelForm
from .models import Scheduler

#モデルを継承したフォーム、P91を参照。modelのクラス名を指定。models.pyで定義した検証するフィールド(今回はdeadlineとtask)を指定。
#これにより、指定した文字数をはみ出していないか、入力必須の項目を入力しているか、型が間違っていないかなどを検証できる。
class SchedulerForm(ModelForm):
    class Meta:
        model   = Scheduler
        fields  = [ "deadline","task" ]

