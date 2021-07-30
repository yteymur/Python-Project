import random
from ortools.graph import pywrapgraph
import pandas as pd
import networkx as nx
import matplotlib as plt
class Program():
    def __init__(self,başlangıç_noktası = [ 0, 0,  0,0,  1,  1, 1,1,1,5,5,5,5,8,8,8,8,0,5,8], bitiş_noktası   = [ 2, 3,  4,7,  2,  3, 4,7,6,2,3,4,6,4,6,7,2,9,9,9],kapasite  = [80, 80, 80,75, 50, 120, 50,60,75,50,50,50,75,65,65,65,65,50,50,50],birim_maliyet  = [ 2, 4,  2,3, 3,  6,  1,4,2,1,1,1,2,1,1,2,1,4,3,2],Üretim_tüketim = [75, 75, -70, -45,-65,75,-60,-20,75,-40],Merkezler= [[0, 2, 80, 2], [0, 3, 80, 4], [0, 4, 80, 2], [0, 7, 75, 3], [1, 2, 50, 3], [1, 3, 120, 6], [1, 4, 50, 1], [1, 7, 60, 4], [1, 6, 75, 2], [5, 2, 50, 1], [5, 3, 50, 1], [5, 4, 50, 1], [5, 6, 75, 2], [8, 4, 65, 1], [8, 6, 65, 1], [8, 7, 65, 2], [8, 2, 65, 1], [0, 9, 50, 4], [5, 9, 50, 3], [8, 9, 50, 2]], Klavuz = { 0 : "İstanbul" , 1 : "Ankara" , 2 : "Eskişehir" , 3  : "Sinop" , 4 : "Sivas" }):
        
        print("NETWORK OLUŞTURULUYOR.......")

        self.bitiş_noktası = bitiş_noktası

        self.başlangıç_noktası = başlangıç_noktası

        self.kapasite = kapasite

        self.birim_maliyet = birim_maliyet
        
        self.Üretim_tüketim = Üretim_tüketim
        self.Merkezler = Merkezler
        self.Klavuz = Klavuz
        
    def MerkezEkle(self):

        while True:
            print("""Bu Sekmede 2 işlem yapılmaktadır...
                     1-Mevcut sistem içinde ekstra bağlantı oluşturmak
                     2-Mevcut sisteme ek üretim veya tüketim merkezi kurmak
                     3-Çıkmak için lütfen 'q' harfine basınız..
                     
                     1. işlemi yapmak için 4 değer vermelisiniz.Bu değerler sırasıyla;
                     Başlama Noktası,Bitiş Noktası,Kapasite ve Birim Maliyettir.
                     Bu değerleri girerken lütfen değerlerin arasına ',' koyunuz.
                     
                     2.İşlemi yapmak için 5 değer vermelisiniz.Bu değerler sırasıyla;
                     Başlama Noktası,Bitiş Noktası,Kapasite,Birim Maliyet ve Üretim-Tüketim değeridir.
                     Bu değerleri girerken lütfen değerlerin arasına ',' koyunuz.
                     !!!UYARI!!!
                     Eğer yeni bir merkez eklemek isterseniz arz-talep dengesini ayarlamanız gerekecektir.
                      """)
            yeni_bir_merkez = input("Yeni Bir Merkez mi Gireceksiniz?(Y/N) İşlemi bitirmek için 'q' ya Basınız:")
            if yeni_bir_merkez == "Y" :
                yeni_merkez_adı =input("Merkezin Kodunu ve İsmini ',' ile ayırarak Giriniz:")
                klavuz_eklenecekler =[]
                klavuz_eklenecekler = yeni_merkez_adı.split(",")
                self.Klavuz[klavuz_eklenecekler[0]] = int(klavuz_eklenecekler[1])
            elif yeni_bir_merkez == "N" :
                pass
            elif yeni_bir_merkez == "q" :
                break
            merkez_bilgileri =input("Lütfen Değerleri Giriniz:")
            if merkez_bilgileri == "q" :
                print(self.Üretim_tüketim)
                for i in range(0,len(self.Merkezler)):
                    print(i+1,". merkez ve değerleri",self.Merkezler[i])
                break
            else:
                eklenecek_merkezler = []
                eklenecek_merkezler = merkez_bilgileri.split(",")
                eklenecek_merkezler = [int(i) for i in eklenecek_merkezler]
                self.başlangıç_noktası.append(eklenecek_merkezler[0])
                self.bitiş_noktası.append(eklenecek_merkezler[1])
                self.kapasite.append(eklenecek_merkezler[2])
                self.birim_maliyet.append(eklenecek_merkezler[3])
                self.Merkezler.append([eklenecek_merkezler[0],eklenecek_merkezler[1],eklenecek_merkezler[2],eklenecek_merkezler[3]])
                print("MERKEZİMİZ EKLENMİŞTİR...")
            try:
                self.Üretim_tüketim.append(eklenecek_merkezler[4])
            except:
                print("Mevcut Bir sistem içine ekstra yol eklediniz...\n")
            if sum(self.Üretim_tüketim) == 0 :
                print("Üretim Devam Ediliyor..\n")
            elif sum(self.Üretim_tüketim) < 0 :
                print("Talepleri Karşılayacak bir üretiminiz yok.Lütfen Üretiminizi {} kadar artırın.".format(abs(sum(self.Üretim_tüketim))))
                for i in range(0,len(self.Üretim_tüketim)):
                   print("{} numaralı Merkezin Üretim-Tüketim Değeri {}'dir".format(i,self.Üretim_tüketim[i]))
                
                yeni_üretim_değerleri=input("Buraya  Değiştirmek İstediğiniz Merkezin İndeksini ve Yeni Değerini Giriniz:")
                eklenecek_değerler =list()
                eklenecek_değerler = yeni_üretim_değerleri.split(",")
                eklenecek_int_değerler = []
                for i in eklenecek_değerler:
                    eklenecek_int_değerler.append(int(i))
                self.Üretim_tüketim[eklenecek_int_değerler[0]] = eklenecek_int_değerler[1]
                print("DEĞERLER GÜNCELLENMİŞTİR...AŞAĞIDAN KONTROL EDEBİLİRSİNİZ.\n")
                for i in range(0,len(self.Üretim_tüketim)):
                   print("{} numaralı Merkezin Üretim-Tüketim Değeri {}'dir\n".format(i,self.Üretim_tüketim[i]))
            elif sum(self.Üretim_tüketim) > 0 :
                print("Taleplerden daha fazla Üretiminiz Mevcuttur.Lütfen Üretim olan merkezlerden birinin üretimi {} kadar azaltınız.\n".format(sum(self.Üretim_tüketim)))
                for i in range(0,len(self.Üretim_tüketim)):
                   print("{} numaralı Merkezin Üretim-Tüketim Değeri {}'dir".format(i,self.Üretim_tüketim[i]))
                yeni_üretim_değerleri2 =input("Buraya Değiştirmek İstediğiniz Merkezin İndeksini Ve Yeni  Değerini Giriniz:")
                eklenecek_değerler2 = []
                eklenecek_değerler2 = yeni_üretim_değerleri2.split(",")
                eklenecek_int_değerler2 =[]
                for i in eklenecek_değerler2:
                    eklenecek_int_değerler2.append(int(i))
                self.Üretim_tüketim[eklenecek_int_değerler2[0]] = eklenecek_int_değerler2[1]
                print("DEĞERLER GÜNCELLENMİŞTİR...AŞAĞIDAN KONTROL EDEBİLİRSİNİZ.\n")
                for i in range(0,len(self.Üretim_tüketim)):
                   print("{} numaralı Merkezin Üretim-Tüketim Değeri {}'dir\n".format(i,self.Üretim_tüketim[i]))
                
           
            
            
            

    def BaglantılarıGöster(self):          
        for i in range(0,len(self.Merkezler)):
            print("Bağlantı   Başlama   Bitiş   Kapasite   Br Mal. ")
            print("{}          {}--------->{}         {}        {}".format(i+1,self.Merkezler[i][0],self.Merkezler[i][1],self.Merkezler[i][2],self.Merkezler[i][3]))
          
    def Problemcöz(self):
        min_cost_flow = pywrapgraph.SimpleMinCostFlow()

        for i in range(0, len(self.başlangıç_noktası)):
            min_cost_flow.AddArcWithCapacityAndUnitCost(self.başlangıç_noktası[i], self.bitiş_noktası[i],
                                                self.kapasite[i], self.birim_maliyet[i])


 

        for i in range(0, len(self.Üretim_tüketim)):
            min_cost_flow.SetNodeSupply(i, self.Üretim_tüketim[i])


        if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
            print('Minimum Maliyet:', min_cost_flow.OptimalCost())
            print('')
            print('  Yol    Akış / Kapasite  Maliyet')
            self.akış=[]
            for i in range(min_cost_flow.NumArcs()):
                self.akış.append(min_cost_flow.Flow(i))
            for i in range(min_cost_flow.NumArcs()):
                cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
                print('%1s -> %1s   %3s  / %3s       %3s' % (
                        min_cost_flow.Tail(i),
                        min_cost_flow.Head(i),
                        min_cost_flow.Flow(i),
                        min_cost_flow.Capacity(i),
                        cost))
        else:
            print('Problem Çözülecek düzeyde değil...')

    def GörselleDestekle(self):
        df = pd.DataFrame({ 'from':self.başlangıç_noktası, 'to':self.bitiş_noktası, 'value': self.akış })
        df['value']=pd.Categorical(df['value'])
        df['value'].cat.codes
        G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph() )
        nx.draw(G, with_labels=True, node_color='red', node_size=1500, edge_color=df["value"].cat.codes, width=5.0, edge_cmap=plt.cm.PuBu)
    

    def Tehditoluştur(self):
        for i in range(0,len(self.Merkezler)):
            print("Bağlantı   Başlama   Bitiş   Kapasite   Br Mal. ")
            print("{}          {}--------->{}         {}        {}".format(i+1,self.Merkezler[i][0],self.Merkezler[i][1],self.Merkezler[i][2],self.Merkezler[i][3]))
        print("\nŞuan Da Görmüş olduğunuz bağlantılardan hangisine tehdit oluşturmak istiyorsunuz?\n")
        Kapasite_değişikliği =input("Tehdit Oluşturmak istediğiniz bağlantının indeksini giriniz ve kapasite değerini giriniz:")
        
        yeni_kapasite_değerleri= []
        yeni_kapasite_değerleri =Kapasite_değişikliği.split(",")
        yeni_kapasite_değerleri2= []
        for i in yeni_kapasite_değerleri :
            yeni_kapasite_değerleri2.append(int(i))
        self.kapasite[yeni_kapasite_değerleri2[0]] = yeni_kapasite_değerleri2[1]
        self.Merkezler[yeni_kapasite_değerleri2[0]][2] = yeni_kapasite_değerleri2[1]
        print("Tehdit oluşturuldu...Kapasiteler değişti.Yeni Durum Aşagıdaki gibi...\n")
        for i in range(0,len(self.Merkezler)):
            print("Bağlantı   Başlama   Bitiş   Kapasite   Br Mal. ")
            print("{}          {}--------->{}         {}        {}".format(i+1,self.Merkezler[i][0],self.Merkezler[i][1],self.Merkezler[i][2],self.Merkezler[i][3]))
            
    def RastgeleTehdit(self):
        
        self.rastgele_index =random.randint(0,len(self.başlangıç_noktası))
        self.rastgele_kapasite = random.choice([0,10,20,30,40])
        self.kapasite[self.rastgele_index] = self.rastgele_kapasite
        self.Merkezler[self.rastgele_index][2] = self.rastgele_kapasite
        print("Rastgele Tehdit Oluşturuldu..")
        for i in range(0,len(self.Merkezler)):
            print("Bağlantı   Başlama   Bitiş   Kapasite   Br Mal. ")
            print("{}          {}--------->{}         {}        {}".format(i+1,self.Merkezler[i][0],self.Merkezler[i][1],self.Merkezler[i][2],self.Merkezler[i][3]))
            
    def KlavuzGoster(self):
        print(self.Klavuz)

Program = Program()
print("""*******************

NETWORK ÇÖZÜM PROGRAMI

İşlemler ;

1.Bağlantı Noktalarını ve değerleri Göster

2.Merkez Ekle

3.Tehdit Oluştur

4.Rastgele Tehdit Oluştur

5.Problemi Çöz

6.Görselle Destekle.

7. Klavuzu Göster.
*******************""")

while True:

    işlem = input("İşlemi Seçiniz:")
    if (işlem == "q"):
        print("Programdan Çıkılıyor...")
        break
    if (işlem == "1"):
        Program.BaglantılarıGöster()
        
    if (işlem == "2"):
        Program.MerkezEkle()
    if (işlem == "3"):
        Program.Tehditoluştur()
    if (işlem == "4"):
        Program.RastgeleTehdit()
    if (işlem == "5"):
        Program.Problemcöz()  
    if (işlem == "6"):
        Program.GörselleDestekle()
    if (işlem == "7") :
        Program.KlavuzGoster()
        
