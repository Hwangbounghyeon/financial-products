from django.db import models
from django.conf import settings

# Create your models here.
class DepositProduct(models.Model):
    type = models.CharField(max_length=255)  # 예금, 적금
    dcls_month = models.CharField(max_length=6)  # 공시 제출월[YYYYMM]
    fin_co_no = models.CharField(max_length=10)  # 금융회사 코드
    fin_prdt_cd = models.CharField(max_length=10)  # 금융상품 코드
    kor_co_nm = models.CharField(max_length=50)  # 금융회사 명
    fin_prdt_nm = models.CharField(max_length=50)  # 금융상품 명
    join_way = models.CharField(max_length=100)  # 가입 방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대 조건
    join_deny = models.IntegerField()  # 가입제한 Ex) 1:제한없음, 2:서민전용, 3:일부제한
    join_member = models.CharField(max_length=50)  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.IntegerField(null=True)  # 최고한도
    dcls_strt_day = models.CharField(max_length=8)  # 공시 시작일 [YYYYMMDD]
    dcls_end_day = models.CharField(max_length=8, null=True)  # 공시 종료일 [YYYYMMDD]
    fin_co_subm_day = models.CharField(max_length=12)  # 금융회사 제출일 [YYYYMMDDHH24MI]


class ProductComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)


class ProductCommentReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_comment = models.ForeignKey(ProductComment, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=255)  # 설명
    
    
class Options(models.Model):
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options')
    dcls_month = models.CharField(max_length=255)  # 공시 제출월 [YYYYMM]
    fin_co_no = models.CharField(max_length=255)  # 금융회사 코드
    fin_prdt_cd = models.CharField(max_length=255)  # 금융상품 코드
    intr_rate_type = models.CharField(max_length=255)  # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=255)  # 저축 금리 유형명
    save_trm = models.CharField(max_length=255)  # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField()  # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField()  # 최고 우대금리 [소수점 2자리]
