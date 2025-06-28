from django import forms
from .models import Recruit
import re

# 基本フォームクラス：すべてのフォームの基底クラス
class BaseRecruitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 必須フィールドにマークを追加
        for field_name, field in self.fields.items():
            if not field.required:
                field.label = f"{field.label}"

    def clean(self):
        cleaned_data = super().clean()
        # 日付フィールドのバリデーション
        for field_name in ['interview_day', 'offer_day', 'offer_hold_date']:
            if field_name in cleaned_data and cleaned_data[field_name]:
                try:
                    cleaned_data[field_name]
                except (ValueError, TypeError):
                    self.add_error(field_name, '有効な日付を入力してください。')
        return cleaned_data

    # 年齢のバリデーション
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None:
            try:
                # 全角数字を半角に変換
                age = int(str(age).translate(str.maketrans('０１２３４５６７８９', '0123456789')))
                if age < 0 or age > 150:
                    raise forms.ValidationError('有効な年齢を入力してください。')
                return age
            except (ValueError, TypeError):
                raise forms.ValidationError('有効な年齢を入力してください。')
        return age

    # 電話番号のバリデーション
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if mobile_number:
            # 全角を半角に変換
            mobile_number = str(mobile_number).translate(str.maketrans('０１２３４５６７８９', '0123456789'))
            # 数字、ハイフン、括弧以外の文字を削除
            mobile_number = re.sub(r'[^\d\-()]', '', mobile_number)
            if len(mobile_number) < 10:
                raise forms.ValidationError('有効な電話番号を入力してください。')
            return mobile_number
        return mobile_number

    # メールアドレスのバリデーション
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                # メールアドレスの形式をチェック
                if '@' not in email or '.' not in email:
                    raise forms.ValidationError('有効なメールアドレスを入力してください。')
                return email
            except Exception:
                raise forms.ValidationError('有効なメールアドレスを入力してください。')
        return email

    class Meta:
        model = Recruit
        fields = []

# 基本情報フォーム：応募者の基本情報を管理
class PersonalInfoForm(BaseRecruitForm):
    # 選考進捗の選択肢
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

    # 提出書類の選択肢
    DOCUMENTS_STATUS_CHOICES = [
        ('', '選択してください'),
        ('提出済み', '提出済み'),
        ('履歴書のみ', '履歴書のみ'),
        ('職務経歴書のみ', '職務経歴書のみ'),
        ('未提出', '未提出'),
    ]

    # オファー結果の選択肢
    OFFER_RESULT_CHOICES = [
        ('', '選択してください'),
        ('合格', '合格'),
        ('不合格', '不合格'),
        ('未', '未'),
    ]

    # 職種の選択肢
    JOB_TITLE_CHOICES = [
        ('', '選択してください'),
        ('エンジニア', 'エンジニア'),
        ('Webデザイナー', 'Webデザイナー'),
        ('クリエイター', 'クリエイター'),
    ]

    # 性別の選択肢
    GENDER_CHOICES = [
        ('', '選択してください'),
        ('男', '男'),
        ('女', '女'),
        ('不明', '不明'),
    ]

    # 都道府県の選択肢
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

    # 基本情報のフィールド定義
    last_name = forms.CharField(
        label='姓',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='名',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name_kana = forms.CharField(
        label='セイ',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name_kana = forms.CharField(
        label='メイ',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        label='選考進捗',
        choices=STATUS_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    document_status = forms.ChoiceField(
        label='提出書類',
        choices=DOCUMENTS_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    document_result = forms.ChoiceField(
        label='書類選考合否',
        choices=Recruit.DOCUMENT_RESULT_CHOICES,
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
    entry_day = forms.DateField(
        label='応募日',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Recruit
        fields = [
            'last_name', 'first_name', 'last_name_kana', 'first_name_kana',
            'status', 'memo', 'job_title', 'entry_day',
            'age', 'mobile_number', 'email', 'gender', 'prefectures', 'address',
            'nationality',
            'document_status',
            'interview_day', 'interview_url', 'interview_reminder_email',
            'interview_reminder_call', 'interview_done', 'interview_result',
            'interviewer', 'interview_feedback',
            'offer_day', 'offer_url', 'offer_reminder_email', 'offer_reminder_call',
            'offer_done', 'offer_result', 'offer_accepted', 'offer_manager',
            'offer_answer', 'offer_hold_date', 'offer_feedback',
            'reference_site', 'unique_question_answer', 'curriculum', 'area',
            'relocation_plan', 'commuting_method', 'time_to_office', 'join_company',
            'parallels_company', 'medical_details', 'final_education', 'learning_level', 'job_change', 'last_job_duration',
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
            'unique_question_answer': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'why_it': forms.TextInput(attrs={'class': 'form-control'}),
            'attraction_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attraction_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attraction_3': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attraction_4': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vision_1': forms.Select(attrs={'class': 'form-select'}),
            'vision_2': forms.Select(attrs={'class': 'form-select'}),
            'vision_3': forms.Select(attrs={'class': 'form-select'}),
            'other_company': forms.TextInput(attrs={'class': 'form-control'}),
            'comparison_points1': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comparison_points2': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'impression': forms.TextInput(attrs={'class': 'form-control'}),
            'grip': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'side_job': forms.TextInput(attrs={'class': 'form-control'}),
        }

# 進捗管理フォーム：選考の進捗状況を管理するフォームクラス
# 書類選考、面接、オファー面談の各段階の情報を管理
class ProgressForm(BaseRecruitForm):
    # 選考進捗のフィールド
    # 応募者の現在の選考ステータスを管理（新規応募、書類選考中、面接中など）
    status = forms.ChoiceField(
        label='選考進捗',
        choices=Recruit.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # 書類選考のフィールド
    # 書類選考の合否結果を管理（合格、不合格、未判定など）
    document_result = forms.ChoiceField(
        label='書類選考合否',
        choices=Recruit.DOCUMENT_RESULT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    # 提出書類の状態を管理（提出済み、履歴書のみ、未提出など）
    document_status = forms.ChoiceField(
        label='提出書類',
        choices=PersonalInfoForm.DOCUMENTS_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # 面接情報のフィールド
    # 面接の実施日を管理
    interview_day = forms.DateField(
        label='面接日',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    # オンライン面接のURLを管理
    interview_url = forms.URLField(
        label='面接URL',
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    # 面接の実施有無を管理（チェックボックス）
    interview_done = forms.BooleanField(
        label='面接実施有無',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    # 面接の合否結果を管理（合格、不合格、未判定など）
    interview_result = forms.ChoiceField(
        label='面接合否',
        choices=Recruit.INTERVIEW_RESULT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # オファー情報のフィールド
    # オファー面談の実施日を管理
    offer_day = forms.DateField(
        label='オファー面談日程',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    # オンラインオファー面談のURLを管理
    offer_url = forms.URLField(
        label='オファー面談URL',
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    # オファー面談の参加有無を管理（チェックボックス）
    offer_done = forms.BooleanField(
        label='オファ面参加有無',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    # オファー面談の結果を管理（合格、不合格、未判定など）
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
    # 内定の承諾有無を管理（チェックボックス）
    offer_accepted = forms.BooleanField(
        label='内定承諾',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # リマインド設定のフィールド
    # 面接前のメールリマインド設定を管理（前日、当日など）
    interview_reminder_email = forms.ChoiceField(
        label='面接リマインドメール',
        choices=Recruit.REMINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    # 面接前の電話リマインド設定を管理（前日、当日など）
    interview_reminder_call = forms.ChoiceField(
        label='面接リマインド電話',
        choices=Recruit.REMINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    # オファー面談前のメールリマインド設定を管理（前日、当日など）
    offer_reminder_email = forms.ChoiceField(
        label='オファー面談リマインドメール',
        choices=Recruit.REMINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    # オファー面談前の電話リマインド設定を管理（前日、当日など）
    offer_reminder_call = forms.ChoiceField(
        label='オファー面談リマインド電話',
        choices=Recruit.REMINDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # その他の情報フィールド
    # 応募媒体を管理（求人サイト、紹介など）
    media = forms.ChoiceField(
        label='媒体',
        choices=Recruit.MEDIA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    # 応募シートの回答有無を管理（チェックボックス）
    sheet_response = forms.BooleanField(
        label='シート回答',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Recruit
        # フォームで使用するフィールドの定義
        fields = [
            'status', 'document_result', 'document_status',
            'interview_day', 'interview_url', 'interview_done', 'interview_result',
            'offer_day', 'offer_url', 'offer_done', 'offer_result', 'offer_accepted',
            'interview_reminder_email', 'interview_reminder_call',
            'offer_reminder_email', 'offer_reminder_call',
            'media', 'sheet_response'
        ]

# 面接報告フォーム：面接の詳細情報を管理
class InterviewReportForm(BaseRecruitForm):
    # カリキュラムの選択肢
    CURRICULUM_CHOICES = [
        ('', '選択してください'),
        ('engineer', 'engineer'),
        ('creator', 'creator'),
    ]

    # エリアの選択肢
    AREA_CHOICES = [
        ('', '選択してください'),
        ('北海道', '北海道'),
        ('宮城', '宮城'),
        ('茨城', '茨城'),
        ('群馬', '群馬'),
        ('東京', '東京'),
        ('新潟', '新潟'),
        ('愛知', '愛知'),
        ('大阪', '大阪'),
        ('広島', '広島'),
        ('福岡', '福岡'),
    ]

    # 面接担当者の選択肢
    INTERVIEWER_CHOICES = [
        ('', '選択してください'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]

    # 最終学歴の選択肢
    FINAL_EDUCATION_CHOICES = [
        ('', '選択してください'),
        ('中卒', '中卒'),
        ('高卒', '高卒'),
        ('高専卒', '高専卒'),
        ('専門卒', '専門卒'),
        ('短期大学', '短期大学'),
        ('大学卒', '大学卒'),
        ('大学院卒', '大学院卒'),
        ('記載なし', '記載なし'),
    ]

    # 学習レベルの選択肢
    LEARNING_LEVEL_CHOICES = [
        ('', '選択してください'),
        ('未経験', '未経験'),
        ('独学', '独学'),
        ('資格（ITパスポート・情報技術者）', '資格（ITパスポート・情報技術者）'),
        ('オンラインスクール', 'オンラインスクール'),
        ('職業訓練校（エンジニア）', '職業訓練校（エンジニア）'),
        ('職業訓練校（デザイン）', '職業訓練校（デザイン）'),
        ('実務経験有り（テスター・インフラ）', '実務経験有り（テスター・インフラ）'),
        ('実務経験有り（業務委託）', '実務経験有り（業務委託）'),
        ('実務経験有り（フロント）', '実務経験有り（フロント）'),
        ('海外で学習経験あり', '海外で学習経験あり'),
        ('大学・専門学校が情報系', '大学・専門学校が情報系'),
        ('未記入', '未記入'),
    ]

    # 転職回数の選択肢
    JOB_CHANGE_CHOICES = [
        ('', '選択してください'),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6回以上', '6回以上'),
        ('新卒', '新卒'),
        ('記載なし', '記載なし'),
    ]

    # 前職期間の選択肢
    LAST_JOB_DURATION_CHOICES = [
        ('', '選択してください'),
        ('新卒', '新卒'),
        ('3ヶ月以内', '3ヶ月以内'),
        ('3-6ヶ月以内', '3-6ヶ月以内'),
        ('6ヶ月-1年', '6ヶ月-1年'),
        ('1年以上', '1年以上'),
        ('2年以上', '2年以上'),
        ('3年以上', '3年以上'),
        ('5年以上', '5年以上'),
    ]

    # TNGの魅力の選択肢
    TNG_ATTRACTION_CHOICES = [
        ('', '選択してください'),
        ('1on1', '1on1'),
        ('チャットのサポート体制', 'チャットのサポート体制'),
        ('24時間365日できる', '24時間365日できる'),
        ('CyTech', 'CyTech'),
        ('いろんな幅がある（Des.Eng.AI）', 'いろんな幅がある（Des.Eng.AI）'),
        ('教育体制', '教育体制'),
        ('研修の手厚さ（期間の長さなど', '研修の手厚さ（期間の長さなど'),
        ('SNS', 'SNS'),
        ('社風', '社風'),
        ('挑戦・成長できる環境', '挑戦・成長できる環境'),
        ('代表の言葉に共感', '代表の言葉に共感'),
        ('社内イベント', '社内イベント'),
        ('MVV・Philosophyに共感', 'MVV・Philosophyに共感'),
        ('地域創生', '地域創生'),
        ('グローバル', 'グローバル'),
        ('キャリアの幅', 'キャリアの幅'),
        ('SDGs', 'SDGs'),
        ('CSV：保護猫活動', 'CSV：保護猫活動'),
        ('CSV：ハートファースト制度', 'CSV：ハートファースト制度'),
        ('評価制度：月間優秀者', '評価制度：月間優秀者'),
        ('人財力100', '人財力100'),
        ('リモート可能', 'リモート可能'),
        ('フレックス可能', 'フレックス可能'),
        ('HPに惹かれた', 'HPに惹かれた'),
        ('動画と資料が良い', '動画と資料が良い'),
        ('未経験9割以上', '未経験9割以上'),
        ('段階を踏んでステップアップ', '段階を踏んでステップアップ'),
        ('地方に支店がある', '地方に支店がある'),
        ('実力主義', '実力主義'),
        ('残業時間少ない', '残業時間少ない'),
        ('福利厚生：上京支援', '福利厚生：上京支援'),
        ('働きながら学習できる', '働きながら学習できる'),
    ]

    # ビジョンの選択肢
    VISION_CHOICES = [
        ('', '選択してください'),
        ('engineer', 'engineer'),
        ('バックエンドエンジニア', 'バックエンドエンジニア'),
        ('PL/PM', 'PL/PM'),
        ('開発やりたい', '開発やりたい'),
        ('Web Designer', 'Web Designer'),
        ('フロントエンドエンジニア', 'フロントエンドエンジニア'),
        ('Web director', 'Web director'),
        ('UI/UX', 'UI/UX'),
        ('marketing', 'marketing'),
        ('人事', '人事'),
        ('creater', 'creater'),
        ('FL', 'FL'),
        ('AI系', 'AI系'),
        ('グローバル&海外PJ', 'グローバル&海外PJ'),
        ('地元/地方盛り上げたい', '地元/地方盛り上げたい'),
        ('教育・教える立場', '教育・教える立場'),
        ('マネジメント', 'マネジメント'),
        ('広報', '広報'),
        ('自社開発に携わりたい', '自社開発に携わりたい'),
        ('企業に貢献', '企業に貢献'),
        ('バックもフロントもできるようになりたい', 'バックもフロントもできるようになりたい'),
        ('マルチに活躍したい', 'マルチに活躍したい'),
        ('サイト制作/0→1で作りたい', 'サイト制作/0→1で作りたい'),
        ('アプリorシステム開発', 'アプリorシステム開発'),
        ('〇〇業界×IT', '〇〇業界×IT'),
        ('月間優秀者', '月間優秀者'),
        ('資格を取りたい', '資格を取りたい'),
        ('これから見つけたい', 'これから見つけたい'),
        ('インフラ', 'インフラ'),
        ('サイテック制覇', 'サイテック制覇'),
        ('リモートワークを実現したい', 'リモートワークを実現したい'),
    ]

    # 面接基本情報
    interview_day = forms.DateField(
        label='面接日',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    interviewer = forms.ChoiceField(
        label='面接担当者',
        choices=INTERVIEWER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    interview_feedback = forms.CharField(
        label='面接所感',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    # 応募者情報
    unique_question_answer = forms.CharField(
        label='ユニークな質問の回答',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    curriculum = forms.ChoiceField(
        label='カリキュラム',
        choices=CURRICULUM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    area = forms.ChoiceField(
        label='エリア',
        choices=AREA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    relocation_plan = forms.CharField(
        label='引越し予定',
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
        label='入社希望日',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    parallels_company = forms.CharField(
        label='並行企業',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    medical_details = forms.CharField(
        label='持病詳細（ある場合のみ記入）',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    final_education = forms.ChoiceField(
        label='最終学歴',
        choices=FINAL_EDUCATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    learning_level = forms.ChoiceField(
        label='学習レベル',
        choices=LEARNING_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    job_change = forms.ChoiceField(
        label='転職回数',
        choices=JOB_CHANGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    last_job_duration = forms.ChoiceField(
        label='直近の仕事の在籍期間',
        choices=LAST_JOB_DURATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    why_it = forms.CharField(
        label='IT業界を志望する理由',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    attraction_1 = forms.ChoiceField(
        label='TNGの魅力1',
        choices=TNG_ATTRACTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    attraction_2 = forms.ChoiceField(
        label='TNGの魅力2',
        choices=TNG_ATTRACTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    attraction_3 = forms.ChoiceField(
        label='TNGの魅力3',
        choices=TNG_ATTRACTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    attraction_4 = forms.ChoiceField(
        label='TNGの魅力4',
        choices=TNG_ATTRACTION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    vision_1 = forms.ChoiceField(
        label='ビジョン1',
        choices=VISION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    vision_2 = forms.ChoiceField(
        label='ビジョン2',
        choices=VISION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    vision_3 = forms.ChoiceField(
        label='ビジョン3',
        choices=VISION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tattoo = forms.BooleanField(
        label='タトゥー有無',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Recruit
        fields = [
            'interview_day', 'interviewer', 'interview_feedback',
            'unique_question_answer', 'curriculum', 'area',
            'relocation_plan', 'commuting_method', 'time_to_office',
            'join_company', 'parallels_company', 'final_education', 'learning_level',
            'job_change', 'last_job_duration', 'why_it',
            'attraction_1', 'attraction_2', 'attraction_3', 'attraction_4',
            'vision_1', 'vision_2', 'vision_3', 'tattoo',
            'medical_details'
        ]

# オファー報告フォーム：オファー面談の詳細情報を管理
class OfferReportForm(BaseRecruitForm):
    # オファー回答の選択肢
    OFFER_ANSWER_CHOICES = [
        ('', '選択してください'),
        ('内定承諾', '内定承諾'),
        ('内定保留', '内定保留'),
        ('お見送り', 'お見送り'),
        ('その場で辞退', 'その場で辞退'),
        ('不参加', '不参加'),
    ]

    # 比較ポイントの選択肢
    COMPARISON_POINTS_CHOICES = [
        ('', '選択してください'),
        ('給与', '給与'),
        ('リモート', 'リモート'),
        ('研修（業務内容）', '研修（業務内容）'),
        ('福利厚生（家賃補助）', '福利厚生（家賃補助）'),
        ('キャリアの幅', 'キャリアの幅'),
        ('会社や面接官の雰囲気', '会社や面接官の雰囲気'),
        ('スキルアップできるか', 'スキルアップできるか'),
        ('学習内容', '学習内容'),
        ('休み', '休み'),
        ('賞与', '賞与'),
        ('研修（期間）', '研修（期間）'),
        ('勤務形態（在宅）', '勤務形態（在宅）'),
        ('入社時期', '入社時期'),
        ('いろんな会社を見たい', 'いろんな会社を見たい'),
        ('休日', '休日'),
        ('やりたいことをやれるか', 'やりたいことをやれるか'),
        ('他業種興味あり', '他業種興味あり'),
        ('その他', 'その他'),
        ('勤務地', '勤務地'),
    ]

    # 性格タイプの選択肢
    PERSONALITY_TYPE_CHOICES = [
        ('', '選択してください'),
        ('明るい', '明るい'),
        ('普通', '普通'),
        ('淡白', '淡白'),
        ('癖あり', '癖あり'),
    ]

    # グリップの選択肢
    GRIP_CHOICES = [
        ('', '選択してください'),
        ('グローバル', 'グローバル'),
        ('サポート', 'サポート'),
        ('インセンティブ賞与', 'インセンティブ賞与'),
        ('キャリカム', 'キャリカム'),
        ('フリーランス支援制度', 'フリーランス支援制度'),
        ('動画編集', '動画編集'),
        ('ゲーム開発', 'ゲーム開発'),
        ('VR開発', 'VR開発'),
        ('社風', '社風'),
    ]

    # オファー面談担当者の選択肢
    OFFER_MANAGER_CHOICES = [
        ('', '選択してください'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    ]

    # 最終カリキュラムの選択肢
    DECISION_CURRICULUM_CHOICES = [
        ('', '選択してください'),
        ('engineer', 'engineer'),
        ('creator', 'creator'),
    ]

    # 国籍の選択肢
    NATIONALITY_CHOICES = [
        ('', '選択してください'),
        ('日本', '日本'),
        ('それ以外', 'それ以外'),
    ]

    # オファー基本情報
    offer_manager = forms.ChoiceField(
        label='オファー面談担当者',
        choices=OFFER_MANAGER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    offer_answer = forms.ChoiceField(
        label='オファー回答',
        choices=OFFER_ANSWER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    offer_hold_date = forms.DateField(
        label='オファー保留期限',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    offer_feedback = forms.CharField(
        label='オファー面談所感',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    # 応募者情報
    other_company = forms.CharField(
        label='他社',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    comparison_points1 = forms.ChoiceField(
        label='比較ポイント1',
        choices=COMPARISON_POINTS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    comparison_points2 = forms.ChoiceField(
        label='比較ポイント2',
        choices=COMPARISON_POINTS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    personality_type = forms.ChoiceField(
        label='性格タイプ',
        choices=PERSONALITY_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    impression = forms.CharField(
        label='感触（業務に難色など）',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    grip = forms.ChoiceField(
        label='グリップ',
        choices=GRIP_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    decision_curriculum = forms.ChoiceField(
        label='最終カリキュラム',
        choices=DECISION_CURRICULUM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    side_job = forms.CharField(
        label='副業',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nationality = forms.ChoiceField(
        label='国籍',
        choices=NATIONALITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
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