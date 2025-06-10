from django.db import models
from datetime import date

# Create your models here.

class Recruit(models.Model):
    # 基本情報
    id = models.AutoField(primary_key=True)
    
    # 選択肢の定義
    STATUS_CHOICES = [
        ('新規応募', '新規応募'),
        ('書類選考NG', '書類選考NG'),
        ('面接調整中', '面接調整中'),
        ('面接確定', '面接確定'),
        ('面接NG', '面接NG'),
        ('オファ面調整中', 'オファ面調整中'),
        ('オファ面確定', 'オファ面確定'),
        ('オファ面NG', 'オファ面NG'),
        ('辞退', '辞退'),
        ('内定承諾', '内定承諾'),
    ]

    DOCUMENT_RESULT_CHOICES = [
        ('', '選択してください'),
        ('合格', '合格'),
        ('書類NG', '書類NG'),
        ('未', '未'),
    ]

    INTERVIEW_RESULT_CHOICES = [
        ('', '選択してください'),
        ('合格', '合格'),
        ('面接NG', '面接NG'),
        ('未', '未'),
    ]

    MEDIA_CHOICES = [
        ('', '選択してください'),
        ('Indeed', 'Indeed'),
        ('Wantedly', 'Wantedly'),
        ('Green', 'Green'),
        ('その他', 'その他'),
    ]

    REMINDER_CHOICES = [
        ('', '選択してください'),
        ('送信済み', '送信済み'),
        ('未送信', '未送信'),
    ]

    status = models.CharField(
        max_length=100,
        verbose_name='選考進捗',
        default='未対応',
        choices=STATUS_CHOICES
    )
    
    memo = models.TextField(blank=True, null=True, verbose_name='備考')
    job_title = models.CharField(max_length=100, blank=True, null=True, verbose_name='職種')
    entry_day = models.DateField(default=date.today, verbose_name='応募日')
    
    # 個人情報
    last_name = models.CharField(max_length=100, verbose_name='姓', default='')
    first_name = models.CharField(max_length=100, verbose_name='名', default='')
    last_name_kana = models.CharField(max_length=100, verbose_name='セイ', default='')
    first_name_kana = models.CharField(max_length=100, verbose_name='メイ', default='')
    age = models.IntegerField(blank=True, null=True, verbose_name='年齢')
    mobile_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='携帯番号')
    email = models.EmailField(blank=True, null=True, verbose_name='メールアドレス')
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='性別')
    prefectures = models.CharField(max_length=50, blank=True, null=True, verbose_name='都道府県')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='現住所')
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='国籍')
    gmail_address = models.EmailField(blank=True, null=True, verbose_name='Gmail')
    
    # 書類選考
    document_result = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='書類選考合否',
        choices=DOCUMENT_RESULT_CHOICES
    )
    
    # 面接情報
    interview_day = models.DateField(blank=True, null=True, verbose_name='面接日程')
    interview_url = models.URLField(blank=True, null=True, verbose_name='URL')
    interview_result = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='面接合否',
        choices=INTERVIEW_RESULT_CHOICES
    )
    interview_reminder_email = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='面接リマインドメール',
        choices=REMINDER_CHOICES
    )
    interview_reminder_call = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='面接リマインド電話',
        choices=REMINDER_CHOICES
    )
    interview_done = models.BooleanField(default=False, verbose_name='面接実施有無')
    interviewer = models.CharField(max_length=100, blank=True, null=True, verbose_name='面接担当者')
    interview_feedback = models.TextField(blank=True, null=True, verbose_name='面接_所感')
    
    # オファー情報
    offer_day = models.DateField(blank=True, null=True, verbose_name='オファー面談日程')
    offer_url = models.URLField(blank=True, null=True, verbose_name='URL')
    offer_accepted = models.BooleanField(default=False, verbose_name='内定')
    offer_reminder_email = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='オファー面談リマインドメール',
        choices=REMINDER_CHOICES
    )
    offer_reminder_call = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='オファー面談リマインド電話',
        choices=REMINDER_CHOICES
    )
    offer_done = models.BooleanField(default=False, verbose_name='オファ面参加有無')
    offer_result = models.CharField(max_length=50, blank=True, null=True, verbose_name='内定')
    offer_manager = models.CharField(max_length=100, blank=True, null=True, verbose_name='オファー面談_担当者')
    offer_answer = models.TextField(blank=True, null=True, verbose_name='オファー面談_回答')
    offer_hold_date = models.DateField(blank=True, null=True, verbose_name='内定保留期日')
    offer_feedback = models.TextField(blank=True, null=True, verbose_name='オファー面談_所感')
    
    # 媒体情報
    media = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='媒体',
        choices=MEDIA_CHOICES
    )
    
    # 参考情報
    reference_site = models.URLField(blank=True, null=True, verbose_name='参考サイト')
    unique_question_answer = models.TextField(blank=True, null=True, verbose_name='ユニークな質問の回答')
    curriculum = models.CharField(max_length=100, blank=True, null=True, verbose_name='カリキュラム')
    area = models.CharField(max_length=100, blank=True, null=True, verbose_name='エリア')
    relocation_plan = models.BooleanField(default=False, verbose_name='引越し予定')
    commuting_method = models.CharField(max_length=100, blank=True, null=True, verbose_name='通勤手段')
    time_to_office = models.CharField(max_length=100, blank=True, null=True, verbose_name='オフィスまでの時間')
    join_company = models.CharField(max_length=100, blank=True, null=True, verbose_name='入社希望時期')
    parallels_company = models.IntegerField(blank=True, null=True, verbose_name='並行数')
    medical_condition = models.BooleanField(default=False, verbose_name='通院/持病')
    medical_details = models.TextField(blank=True, null=True, verbose_name='詳細')
    final_education = models.CharField(max_length=200, blank=True, null=True, verbose_name='最終学歴')
    learning_level = models.CharField(max_length=100, blank=True, null=True, verbose_name='入社前学習レベル')
    job_change = models.IntegerField(blank=True, null=True, verbose_name='転職回数')
    last_job_duration = models.CharField(max_length=100, blank=True, null=True, verbose_name='直近の仕事の在籍期間')
    why_it = models.TextField(blank=True, null=True, verbose_name='ITへ転職経緯')
    
    # TNG関連
    attraction_1 = models.TextField(blank=True, null=True, verbose_name='TNGの魅力1')
    attraction_2 = models.TextField(blank=True, null=True, verbose_name='TNGの魅力2')
    attraction_3 = models.TextField(blank=True, null=True, verbose_name='TNGの魅力3')
    attraction_4 = models.TextField(blank=True, null=True, verbose_name='TNGの魅力4')
    vision_1 = models.TextField(blank=True, null=True, verbose_name='ビジョン1')
    vision_2 = models.TextField(blank=True, null=True, verbose_name='ビジョン2')
    vision_3 = models.TextField(blank=True, null=True, verbose_name='ビジョン3')
    
    # その他
    tattoo = models.BooleanField(default=False, verbose_name='タトゥー')
    other_company = models.TextField(blank=True, null=True, verbose_name='他社選考数')
    comparison_points1 = models.TextField(blank=True, null=True, verbose_name='他社比較ポイント1')
    comparison_points2 = models.TextField(blank=True, null=True, verbose_name='他社比較ポイント2')
    personality_type = models.CharField(max_length=100, blank=True, null=True, verbose_name='性格タイプ')
    impression = models.TextField(blank=True, null=True, verbose_name='感触')
    grip = models.TextField(blank=True, null=True, verbose_name='グリップ')
    decision_curriculum = models.CharField(max_length=100, blank=True, null=True, verbose_name='カリキュラム')
    side_job = models.TextField(blank=True, null=True, verbose_name='副業相談')
    sheet_response = models.BooleanField(default=False, verbose_name='シート回答')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = '応募者'
        verbose_name_plural = '応募者'

