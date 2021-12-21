# 1. Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.
import pandas as pd
import seaborn as sns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
df=pd.read_excel("online_retail_II.xlsx",sheet_name="Year 2010-2011")
dff=df.copy()
# 2. Veri setinin betimsel istatistiklerini inceleyiniz.
dff.head()
dff.describe().T
dff.shape
# 3. Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?
dff.isnull().values.any()
dff.isnull().sum()
# 4. Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.
dff.dropna(inplace=True)
dff.isnull().sum()
# 5. Eşsiz ürün sayısı kaçtır?
dff["Description"].nunique()
# 6. Hangi üründen kaçar tane vardır?
dff["Description"].value_counts()
# 7. En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız.
dff.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(5)
# 8. Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız.
dff=dff[~dff["Invoice"].str.contains("C",na=False)]
#Soru9:Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz.
dff["TotalPrice"]=dff["Price"]*dff["Quantity"]
# Görev 2:
# RFM metriklerinin hesaplanması
# ▪ Recency, Frequency ve Monetary tanımlarını yapınız.
# ▪ Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile
# hesaplayınız.
# ▪ Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.
# ▪ Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.
# RFM metriklerinin hesaplanması
# İpucu:
# Görev 2:
# Not 1: recency değeri için bugünün tarihini (2011, 12, 11) olarak kabul ediniz.
# Not 2: rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz.
import datetime as dt
today_date = dt.datetime(2011, 12, 11)
rfm = dff.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
rfm.columns = ['recency', 'frequency', "monetary"]
rfm = rfm[(rfm['monetary'] > 0)]
#GÖREV 3
#RFM skorlarının oluşturulması ve tek bir değişkene çevrilmesi

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm['rfm_score'] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)
#GÖREV 4
#RFM skorlarının segment olarak tanımlanması
seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

rfm['segment'] = rfm['rfm_score'].replace(seg_map, regex=True)
rfm = rfm[["recency", "frequency", "monetary", "segment"]]
#GÖREV 5
#Önemli bulduğunuz 3 segmenti seçiniz. Bu üç segmenti;
# Hem aksiyon kararları açısından,
# Hem de segmentlerin yapısı açısından (ortalama RFM değerleri) yorumlayınız.
#"Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.

rfm_karsilastirma=rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])
# cant_loose segmentindeki müşteriler son zamanlarda alışveriş yapmamış olsalar da getiri bakımından üst seviye müşteri kitlesi.
# Geri kazanımları şirket için etkili olur.at_risk ve potential_loyalist segmentleri getiri açısından yüksek seviye olan bir
# diğer müşteri kitlesi. Bunlar da ürün gamları genişletilerek veya promosyonlar ile tekrar şirkete müşteri olarak kazandırılabilir
# ve alışveriş sıklıkları arttırılabilinir.






rfm_akin=rfm[rfm["segment"] == "loyal_customers"]
rfm_akin.to_excel("loyal_customers.xlsx")
