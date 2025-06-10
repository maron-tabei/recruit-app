from django import forms
from .models import Recruit
import re

class BaseRecruitForm(forms.ModelForm):
    # 全角数字を半角に変換する関数
    def to_half_width(self, value):
        if value is None:
            return value
        # 全角数字を半角に変換
        value = str(value)
        value = value.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
        # 全角スペースを半角に変換
        value = value.translate(str.maketrans('　', ' '))
        # 全角ハイフンや括弧を半角に変換
        value = value.translate(str.maketrans('－（）', '-()'))
        return value

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age:
            # 文字列に変換して全角を半角に変換
            age_str = self.to_half_width(str(age))
            # 数字以外の文字を削除
            age_str = re.sub(r'[^\d]', '', age_str)
            try:
                return int(age_str)
            except ValueError:
                raise forms.ValidationError('有効な年齢を入力してください。')
        return age

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if mobile_number:
            # 全角を半角に変換
            mobile_number = self.to_half_width(mobile_number)
            # 数字、ハイフン、括弧以外の文字を削除
            mobile_number = re.sub(r'[^\d\-()]', '', mobile_number)
            return mobile_number
        return mobile_number

    class Meta:
        model = Recruit
        fields = []

class PersonalInfoForm(BaseRecruitForm):
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

    DOCUMENTS_STATUS_CHOICES = [
        ('', '選択してください'),
        ('提出済み', '提出済み'),
        ('履歴書のみ', '履歴書のみ'),
        ('職務経歴書のみ', '職務経歴書のみ'),
        ('未提出', '未提出'),
    ]

    OFFER_RESULT_CHOICES = [
        ('', '選択してください'),
        ('合格', '合格'),
        ('不合格', '不合格'),
        ('未', '未'),
    ]

    JOB_TITLE_CHOICES = [
        ('', '選択してください'),
        ('エンジニア', 'エンジニア'),
        ('Webデザイナー', 'Webデザイナー'),
        ('クリエイター', 'クリエイター'),
    ]

    GENDER_CHOICES = [
        ('', '選択してください'),
        ('男', '男'),
        ('女', '女'),
        ('不明', '不明'),
    ]

    PREFECTURE_CHOICES = [
        ('', '選択してください'),
        ('北海道', '北海道'),
        ('青森県', '青森県'),
        ('岩手県', '岩手県'),
        ('宮城県', '宮城県'),
        ('秋田県', '秋田県'),
        ('山形県', '山形県'),
        ('福島県', '福島県'),
        ('茨城県', '茨城県'),
        ('栃木県', '栃木県'),
        ('群馬県', '群馬県'),
        ('埼玉県', '埼玉県'),
        ('千葉県', '千葉県'),
        ('東京都', '東京都'),
        ('神奈川県', '神奈川県'),
        ('新潟県', '新潟県'),
        ('富山県', '富山県'),
        ('石川県', '石川県'),
        ('福井県', '福井県'),
        ('山梨県', '山梨県'),
        ('長野県', '長野県'),
        ('岐阜県', '岐阜県'),
        ('静岡県', '静岡県'),
        ('愛知県', '愛知県'),
        ('三重県', '三重県'),
        ('滋賀県', '滋賀県'),
        ('京都府', '京都府'),
        ('大阪府', '大阪府'),
        ('兵庫県', '兵庫県'),
        ('奈良県', '奈良県'),
        ('和歌山県', '和歌山県'),
        ('鳥取県', '鳥取県'),
        ('島根県', '島根県'),
        ('岡山県', '岡山県'),
        ('広島県', '広島県'),
        ('山口県', '山口県'),
        ('徳島県', '徳島県'),
        ('香川県', '香川県'),
        ('愛媛県', '愛媛県'),
        ('高知県', '高知県'),
        ('福岡県', '福岡県'),
        ('佐賀県', '佐賀県'),
        ('長崎県', '長崎県'),
        ('熊本県', '熊本県'),
        ('大分県', '大分県'),
        ('宮崎県', '宮崎県'),
        ('鹿児島県', '鹿児島県'),
        ('沖縄県', '沖縄県'),
    ]

    last_name = forms.CharField(
        label='姓',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='名',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name_kana = forms.CharField(
        label='セイ',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name_kana = forms.CharField(
        label='メイ',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        label='選考進捗',
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    document_status = forms.ChoiceField(
        label='提出書類',
        choices=DOCUMENTS_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    job_title = forms.ChoiceField(
        label='職種',
        choices=JOB_TITLE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        label='性別',
        choices=GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    prefectures = forms.ChoiceField(
        label='都道府県',
        choices=PREFECTURE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        label='年齢',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    mobile_number = forms.CharField(
        label='携帯電話番号',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='メールアドレス',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='住所',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    memo = forms.CharField(
        label='メモ',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = Recruit
        fields = [
            'last_name', 'first_name', 'last_name_kana', 'first_name_kana',
            'status', 'memo', 'job_title', 'entry_day',
            'age', 'mobile_number', 'email', 'gender', 'prefectures', 'address',
            'nationality', 'gmail_address',
            'document_status',
            'interview_day', 'interview_url', 'interview_reminder_email',
            'interview_reminder_call', 'interview_done', 'interview_result',
            'interviewer', 'interview_feedback',
            'offer_day', 'offer_url', 'offer_reminder_email', 'offer_reminder_call',
            'offer_done', 'offer_result', 'offer_accepted', 'offer_manager',
            'offer_answer', 'offer_hold_date', 'offer_feedback',
            'reference_site', 'unique_question_answer', 'curriculum', 'area',
            'relocation_plan', 'commuting_method', 'time_to_office', 'join_company',
            'parallels_company', 'medical_condition', 'medical_details',
            'final_education', 'learning_level', 'job_change', 'last_job_duration',
            'why_it',
            'attraction_1', 'attraction_2', 'attraction_3', 'attraction_4',
            'vision_1', 'vision_2', 'vision_3',
            'tattoo', 'other_company', 'comparison_points1', 'comparison_points2',
            'personality_type', 'impression', 'grip', 'decision_curriculum',
            'side_job', 'media', 'sheet_response'
        ]
        widgets = {
            'entry_day': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'interview_day': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'offer_day': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'offer_hold_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'interview_feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'offer_feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'unique_question_answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medical_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'why_it': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attraction_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attraction_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attraction_3': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attraction_4': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vision_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vision_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vision_3': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'other_company': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comparison_points1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comparison_points2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'impression': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'grip': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'side_job': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProgressForm(BaseRecruitForm):
    status = forms.ChoiceField(
        label='選考進捗',
        choices=Recruit.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    document_result = forms.ChoiceField(
        label='書類選考合否',
        choices=Recruit.DOCUMENT_RESULT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    document_status = forms.ChoiceField(
        label='提出書類',
        choices=PersonalInfoForm.DOCUMENTS_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    interview_day = forms.DateField(
        label='面接日',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    interview_url = forms.URLField(
        label='面接URL',
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    interview_done = forms.BooleanField(
        label='面接実施有無',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    interview_result = forms.ChoiceField(
        label='面接合否',
        choices=Recruit.INTERVIEW_RESULT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    offer_day = forms.DateField(
        label='オファー面談日程',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    offer_url = forms.URLField(
        label='オファー面談URL',
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    offer_done = forms.BooleanField(
        label='オファ面参加有無',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    offer_result = forms.ChoiceField(
        label='内定',
        required=False,
        choices=[
            ('', '選択してください'),
            ('合格', '合格'),
            ('不合格', '不合格'),
            ('未', '未'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    offer_accepted = forms.BooleanField(
        label='内定承諾',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    media = forms.ChoiceField(
        label='媒体',
        choices=Recruit.MEDIA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sheet_response = forms.BooleanField(
        label='シート回答',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    interview_reminder_email = forms.ChoiceField(
        label='面接リマインドメール',
        choices=Recruit.REMINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    interview_reminder_call = forms.ChoiceField(
        label='面接リマインド電話',
        choices=Recruit.REMINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    offer_reminder_email = forms.ChoiceField(
        label='オファー面談リマインドメール',
        choices=Recruit.REMINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    offer_reminder_call = forms.ChoiceField(
        label='オファー面談リマインド電話',
        choices=Recruit.REMINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Recruit
        fields = [
            'status', 'document_result', 'document_status', 'interview_day',
            'interview_url', 'interview_done', 'interview_result', 'offer_day',
            'offer_url', 'offer_done', 'offer_result', 'offer_accepted',
            'media', 'sheet_response', 'interview_reminder_email',
            'interview_reminder_call', 'offer_reminder_email', 'offer_reminder_call'
        ]

class InterviewReportForm(BaseRecruitForm):
    interview_day = forms.DateField(
        label='面接日',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    interviewer = forms.CharField(
        label='面接担当者',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    interview_feedback = forms.CharField(
        label='面接フィードバック',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    unique_question_answer = forms.CharField(
        label='ユニークな質問の回答',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    curriculum = forms.CharField(
        label='カリキュラム',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    area = forms.CharField(
        label='エリア',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    relocation_plan = forms.CharField(
        label='転居予定',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    commuting_method = forms.CharField(
        label='通勤手段',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    time_to_office = forms.CharField(
        label='通勤時間',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    join_company = forms.CharField(
        label='入社予定日',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    parallels_company = forms.CharField(
        label='並行企業',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    medical_condition = forms.CharField(
        label='健康状態',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    medical_details = forms.CharField(
        label='健康状態詳細',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    final_education = forms.CharField(
        label='最終学歴',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    learning_level = forms.CharField(
        label='学習レベル',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    job_change = forms.CharField(
        label='転職回数',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_job_duration = forms.CharField(
        label='前職期間',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    why_it = forms.CharField(
        label='IT業界を志望する理由',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    attraction_1 = forms.CharField(
        label='TNGの魅力1',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    attraction_2 = forms.CharField(
        label='TNGの魅力2',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    attraction_3 = forms.CharField(
        label='TNGの魅力3',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    attraction_4 = forms.CharField(
        label='TNGの魅力4',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    vision_1 = forms.CharField(
        label='ビジョン1',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    vision_2 = forms.CharField(
        label='ビジョン2',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    vision_3 = forms.CharField(
        label='ビジョン3',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    tattoo = forms.CharField(
        label='タトゥー',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Recruit
        fields = [
            'interview_day', 'interviewer', 'interview_feedback', 'unique_question_answer',
            'curriculum', 'area', 'relocation_plan', 'commuting_method',
            'time_to_office', 'join_company', 'parallels_company',
            'medical_condition', 'medical_details', 'final_education',
            'learning_level', 'job_change', 'last_job_duration', 'why_it',
            'attraction_1', 'attraction_2', 'attraction_3', 'attraction_4',
            'vision_1', 'vision_2', 'vision_3', 'tattoo'
        ]

class OfferReportForm(BaseRecruitForm):
    offer_manager = forms.CharField(
        label='オファー面談担当者',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    offer_answer = forms.CharField(
        label='オファー回答',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    offer_hold_date = forms.DateField(
        label='オファー保留期限',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    offer_feedback = forms.CharField(
        label='オファー面談フィードバック',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    other_company = forms.CharField(
        label='他社',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    comparison_points1 = forms.CharField(
        label='比較ポイント1',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    comparison_points2 = forms.CharField(
        label='比較ポイント2',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    personality_type = forms.CharField(
        label='性格タイプ',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    impression = forms.CharField(
        label='印象',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    grip = forms.CharField(
        label='グリップ',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    decision_curriculum = forms.CharField(
        label='決定カリキュラム',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    side_job = forms.CharField(
        label='副業',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    nationality = forms.CharField(
        label='国籍',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gmail_address = forms.EmailField(
        label='Gmailアドレス',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Recruit
        fields = [
            'offer_manager', 'offer_answer', 'offer_hold_date',
            'offer_feedback', 'other_company', 'comparison_points1',
            'comparison_points2', 'personality_type', 'impression',
            'grip', 'decision_curriculum', 'side_job', 'nationality',
            'gmail_address'
        ] 