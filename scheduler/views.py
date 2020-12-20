from django.shortcuts import render,redirect

from django.views import View

#models.pyで定義したSchedulerをimportする
from .models import Scheduler

from .forms import SchedulerForm,SchedulerDeleteForm


#P35のビュー関数の書き方(関数ベース vs クラスベース)を参照。後の汎用性も考慮しクラスベースのビューを採用した。
class SchedulerView(View):

    def get(self ,request, *args, **kwargs):

        #.all()メソッドを使用することでDBに格納されているSchedulerのデータを全て抽出できる(P57)
        #.order_by()メソッドを使い、並び替えをする(P61)
        data    = Scheduler.objects.all().order_by("deadline")
        context = { "data":data }
        
        return render(request, "scheduler/index.html", context)

    def post(self ,request, *args, **kwargs):

        #クライアントから受け取ったデータをDBに格納する。(P62)
        """
        posted  = Scheduler(  deadline    = request.POST["deadline"],
                              task        = request.POST["task"]    )
        posted.save()
        """

        #ここに送信されたデータがSchedulerFormに引数として与えられ、.is_valid()でバリデーションを行う。P87のビューでの利用例を参照
        formset = SchedulerForm(request.POST)
        
        #バリデーションOKの場合、Trueが返ってくる。
        if formset.is_valid():
            #モデルを継承して作ったformsのクラスの場合、.save()メソッドを使うことでDBに保存できる。
            formset.save()
        else:
            print("バリデーションエラー")


        return redirect("scheduler:index")

#クラスで記述したビューを関数化するための処理。これによりurls.pyから呼び出せる
index   = SchedulerView.as_view()


#指定したスケジュールを削除するクラス
class SchedulerDelete(View):

    def post(self ,request, *args, **kwargs):

        #削除対象のレコードをIDで一意に特定する。.delete()で削除
        """
        posted  = Scheduler.objects.filter(id=request.POST["id"])
        posted.delete()
        """

        #バリデーションを行う
        formset = SchedulerDeleteForm(request.POST)

        #バリデーションが適切であれば削除処理、そうでなければエラー表示
        if formset.is_valid():

            #バリデーションした後の値を取り出す
            clean_data  = formset.clean()

            #filterで絞り込み、.delete()で削除処理をする。
            Scheduler.objects.filter(id=clean_data["id"]).delete()

        else:
            print("バリデーションエラー")


        return redirect("scheduler:index")
   
delete  = SchedulerDelete.as_view()
