# 7Dimensions MCP AI Server Dokümantasyonu

## 📋 Genel Bakış

7Dimensions AI Server, **Model Context Protocol (MCP)** kullanarak BIM modellerini analiz eden ve **Identity Data** sorularını yanıtlayan gelişmiş bir AI sistemidir. Bu sistem, Autodesk Viewer ile entegre çalışarak proje yönetimi ve BIM analizi için kapsamlı destek sunar.

## 🔧 Sistem Mimarisi

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   MCP Tools     │    │   AI Service    │
│  (ApsViewer.js) │────▶│ (mcp-tools.js)  │────▶│ (aiService.js)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       ▼
         │              ┌─────────────────┐    ┌─────────────────┐
         │              │  Identity Data  │    │   OpenRouter    │
         └──────────────▶│    Analysis     │    │      API        │
                        └─────────────────┘    └─────────────────┘
```

## 🚀 Kurulum ve Konfigürasyon

### Gereksinimler
- Node.js v16+
- Autodesk Viewer SDK
- OpenRouter API Key (DeepSeek Chat modeli)

### Environment Değişkenleri
```bash
OPENROUTER_API_KEY=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
```

## 📊 Identity Data Alanları

Sistem aşağıdaki **8 kritik Identity Data alanını** destekler:

| Alan Adı | Açıklama | Örnek Değer |
|----------|----------|-------------|
| **Edited by** | Son düzenleyen kişi | "Ali Yılmaz" |
| **Alt Yüklenici** | İşi yapan alt yüklenici firma | "XYZ İnşaat" |
| **İşveren Hakediş No** | İşveren hakediş numarası | "3" |
| **Alt Yüklenici Hakediş No** | Alt yüklenici hakediş numarası | "2" |
| **İmalat Tarihi** | İmalatın yapıldığı tarih | "2024-11-15" |
| **Activity ID** | Faaliyet kimlik numarası | "ACT-3042" |
| **İlerleme** | Tamamlanma yüzdesi | "%75" |
| **Müşavir Onay Durumu** | Müşavir onay durumu | "Onaylandı" |

## 🔧 MCP Tools Fonksiyonları

### 1. Temel Identity Data Fonksiyonları

#### `getElementIdentityData(dbId)`
Belirli bir element için Identity Data bilgilerini getirir.

**Parametreler:**
- `dbId`: Element ID'si (string/number)

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "name": "Element Adı",
    "category": "Kategori",
    "identityData": {
      "Alt Yüklenici": "XYZ İnşaat",
      "İlerleme": "%75",
      "Müşavir Onay Durumu": "Onaylandı"
    }
  },
  "message": "Element bilgileri başarıyla getirildi"
}
```

#### `queryIdentityField(fieldName, value?)`
Identity Data alanlarına göre sorgu yapar.

**Parametreler:**
- `fieldName`: Sorgulanacak alan adı (string)
- `value`: Aranan değer (string, opsiyonel)

**Örnek Kullanım:**
```javascript
queryIdentityField("Alt Yüklenici", "XYZ")
queryIdentityField("İmalat Tarihi")
```

### 2. Analiz Fonksiyonları

#### `getContractorElements(contractorName?)`
Alt yüklenici bazında elementleri listeler.

**Dönen Değer:**
```json
{
  "success": true,
  "data": [
    {
      "dbId": "123",
      "name": "Element Adı",
      "category": "Walls",
      "contractor": "XYZ İnşaat",
      "progress": "%75",
      "approvalStatus": "Onaylandı",
      "activityId": "ACT-3042"
    }
  ],
  "count": 45,
  "message": "XYZ İnşaat için 45 element bulundu"
}
```

#### `getProgressSummary()`
Tüm elementlerin ilerleme durumu özetini getirir.

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "%0": { "count": 12, "elements": [...] },
    "%25": { "count": 8, "elements": [...] },
    "%50": { "count": 15, "elements": [...] },
    "%75": { "count": 20, "elements": [...] },
    "%100": { "count": 35, "elements": [...] }
  },
  "totalElements": 90,
  "message": "90 element için ilerleme durumu analiz edildi"
}
```

#### `getApprovalStatus()`
Müşavir onay durumu analizini getirir.

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "Onaylandı": { "count": 45, "elements": [...] },
    "Beklemede": { "count": 25, "elements": [...] },
    "Reddedildi": { "count": 5, "elements": [...] }
  },
  "totalElements": 75,
  "message": "75 element için onay durumu analiz edildi"
}
```

#### `getPaymentRequestSummary()`
Hakediş numaralarına göre özet getirir.

**Dönen Değer:**
```json
{
  "success": true,
  "data": {
    "ownerRequests": {
      "1": { "count": 20, "elements": [...] },
      "2": { "count": 15, "elements": [...] },
      "3": { "count": 10, "elements": [...] }
    },
    "contractorRequests": {
      "1": { "count": 18, "elements": [...] },
      "2": { "count": 12, "elements": [...] }
    }
  },
  "totalElements": 75,
  "message": "75 element için hakediş analizi tamamlandı"
}
```

### 3. Vurgulama Fonksiyonları

#### `highlightByIdentityField(fieldName, value)`
Identity Data alanına göre elementleri vurgular.

**Parametreler:**
- `fieldName`: Alan adı (string)
- `value`: Değer (string)

**Dönen Değer:**
```json
{
  "success": true,
  "type": "highlight",
  "data": {
    "dbIds": [123, 456, 789],
    "categoryName": "Alt Yüklenici: XYZ İnşaat"
  },
  "count": 3,
  "message": "Alt Yüklenici = XYZ İnşaat için 3 element vurgulandı"
}
```

### 4. Grafik Üretim Fonksiyonları (📊 Power BI Tarzı)

#### `generateCategoryChart(chartType)`
Kategori sayılarına göre pasta/bar grafiği oluşturur.

**Parametreler:**
- `chartType`: 'pie' veya 'bar' (string)

**Dönen Değer:**
```json
{
  "instruction": "frontend_chart",
  "chartData": {
    "type": "pie",
    "labels": ["Duvarlar", "Kapılar", "Pencereler", "Kolonlar"],
    "values": [180, 100, 24, 176],
    "label": "Kategori Element Sayıları"
  },
  "message": "Kategori dağılımı (4 kategori, 480 toplam element)"
}
```

#### `generateProgressChart()`
İlerleme durumuna göre pasta grafiği oluşturur.

**Dönen Değer:**
```json
{
  "instruction": "frontend_chart",
  "chartData": {
    "type": "pie", 
    "labels": ["%0", "%25", "%50", "%75", "%100"],
    "values": [12, 8, 15, 20, 35],
    "label": "İlerleme Durumu"
  },
  "message": "İlerleme durumu dağılımı (90 element)"
}
```

#### `generateContractorChart()`
Alt yüklenicilere göre bar grafiği oluşturur.

**Dönen Değer:**
```json
{
  "instruction": "frontend_chart",
  "chartData": {
    "type": "bar",
    "labels": ["XYZ İnşaat", "ABC Yapı", "DEF Müteahhit"],
    "values": [45, 32, 18],
    "label": "Alt Yüklenici Dağılımı"
  },
  "message": "Alt yüklenici dağılımı (3 yüklenici, 95 element)"
}
```

**Grafik Özellikleri:**
- ✅ **İnteraktif Tooltips** - Hover'da detaylı bilgi + yüzde hesaplama
- ✅ **Grafik Türü Değiştirme** - Pasta ↔ Bar grafiği arası geçiş
- ✅ **PNG İndirme** - Grafikleri PNG olarak kaydetme
- ✅ **Responsive Design** - Mobil uyumlu grafikler
- ✅ **Profesyonel Renkler** - Power BI tarzı renk paleti
- ✅ **Otomatik Scaling** - Verilere göre otomatik ölçeklendirme

## 🗣️ Desteklenen Doğal Dil Sorguları

### Identity Data Sorguları

#### Alt Yüklenici Sorguları
- ❓ **"Bu eleman hangi alt yüklenici tarafından yapılmış?"**
- ❓ **"Hangi alt yükleniciler çalışmış?"**
- ❓ **"XYZ İnşaat kaç tane element yapmış?"**
- ❓ **"Alt yüklenicileri listele"**

#### İmalat Tarihi Sorguları
- ❓ **"İmalat tarihi nedir?"**
- ❓ **"Bu eleman ne zaman yapılmış?"**
- ❓ **"2024-11-15 tarihinde ne yapılmış?"**

#### Onay Durumu Sorguları
- ❓ **"Bu imalat onaylanmış mı?"**
- ❓ **"Müşavir onay durumu nasıl?"**
- ❓ **"Hangi işler onay bekliyor?"**
- ❓ **"Reddedilen elementler var mı?"**

#### İlerleme Durumu Sorguları
- ❓ **"İlerleme yüzdesi nedir?"**
- ❓ **"Proje yüzde kaç tamamlandı?"**
- ❓ **"Hangi işler %100 bitti?"**
- ❓ **"İlerleme durumu nasıl?"**

#### Hakediş Sorguları
- ❓ **"İşveren hakediş numarası kaç?"**
- ❓ **"Hakediş durumu nedir?"**
- ❓ **"3 numaralı hakediş kapsamında neler var?"**

#### Activity ID Sorguları
- ❓ **"Activity ID nedir?"**
- ❓ **"ACT-3042 faaliyeti nedir?"**
- ❓ **"Bu elementin faaliyet numarası kaç?"**

### Kategori ve Sayı Sorguları

#### Element Sayı Sorguları
- ❓ **"Kaç tane duvar var?"**
- ❓ **"Pencere sayısı nedir?"** 
- ❓ **"Kapı sayısını göster"**
- ❓ **"Toplam element sayısı kaç?"**

#### Kategori Sorguları
- ❓ **"Kategorileri listele"**
- ❓ **"Hangi kategoriler var?"**

#### Grafik ve Analiz Sorguları (📊 Power BI Tarzı)

**Kategori Grafikler:**
- ❓ **"Element sayılarına göre pasta grafiği çıkar"**
- ❓ **"Kategorilere göre bar grafiği oluştur"**
- ❓ **"Kategori dağılımı grafiği"**
- ❓ **"Element analizi grafiği"**
- ❓ **"Pasta grafik çıkart"**
- ❓ **"Bar chart yap"**
- ❓ **"Kategori görselleştir"**
- ❓ **"Power BI tarzı analiz"**

**İlerleme Grafikler:**
- ❓ **"İlerleme durumu grafiği"**
- ❓ **"Proje ilerleme analizi"**
- ❓ **"Tamamlanma oranları grafiği"**
- ❓ **"Progress chart"**

**Yüklenici Grafikler:**
- ❓ **"Alt yüklenici dağılımı grafiği"**
- ❓ **"Firmalar bazında analiz"**
- ❓ **"Contractor distribution"**
- ❓ **"Yüklenici karşılaştırması"**

**Genel Analiz:**
- ❓ **"Proje analizini görselleştir"**
- ❓ **"Dashboard oluştur"**
- ❓ **"İstatistiksel analiz"**
- ❓ **"Grafik analizi yap"**

### Vurgulama Komutları

#### Kategori Bazlı Yalıtma (Isolate)

**Tekli Kategoriler:**
- ❓ **"Duvarları göster"** - Sadece duvarları görünür kılar
- ❓ **"Pencereleri göster"** - Sadece pencereleri görünür kılar  
- ❓ **"Kapıları göster"** - Sadece kapıları görünür kılar
- ❓ **"Kolonları göster"** - Sadece kolonları görünür kılar
- ❓ **"Çatıları göster"** - Sadece çatıları görünür kılar
- ❓ **"Mobilyaları göster"** - Sadece mobilyaları görünür kılar
- ❓ **"Merdivenleri göster"** - Sadece merdivenleri görünür kılar
- ❓ **"Tesisat göster"** - Sadece tesisat elemanlarını görünür kılar

**Çoklu Kategoriler (Birden Fazla):**
- ❓ **"Kapı ve pencere göster"** - Kapı + pencere kategorilerini birlikte gösterir
- ❓ **"Duvar ve çatı göster"** - Duvar + çatı kategorilerini birlikte gösterir
- ❓ **"Kolon ve kiriş göster"** - Yapısal elemanları birlikte gösterir
- ❓ **"Kapı pencere merdiven göster"** - 3 kategoriyi birlikte gösterir
- ❓ **"Mobilya ve tesisat göster"** - MEP + mobilya elemanlarını gösterir

**Farklı İfadeler:**
- ❓ **"Sadece duvarları göster"** - Diğer kategorileri gizler
- ❓ **"Yalnızca pencereler"** - Sadece pencereler görünür
- ❓ **"Show walls"** - İngilizce komutlar da desteklenir
- ❓ **"Display columns"** - İngilizce görüntüleme komutu

**Tümünü Göster:**
- ❓ **"Tümünü göster"** - Tüm kategorileri tekrar görünür kılar
- ❓ **"Hepsini göster"** - Yalıtmayı kaldırır
- ❓ **"Temizle"** - Filtreleri temizler

#### Identity Data Bazlı Yalıtma  
- ❓ **"XYZ İnşaat'ın yaptığı elementleri göster"** - Sadece o firma elementleri
- ❓ **"Onaylanmış elementleri göster"** - Sadece onaylı elementler
- ❓ **"%100 tamamlanan işleri göster"** - Sadece tamamlanan işler
- ❓ **"3 numaralı hakedişteki elementleri göster"** - Sadece o hakediş elementleri

#### Tüm Elementleri Gösterme
- ❓ **"Tümünü göster"** - Tüm elementleri görünür kılar
- ❓ **"Hepsini göster"** - Model browser'daki "Show All" gibi
- ❓ **"Temizle"** - Yalıtmayı kaldırır

## 🔄 Sistem Akışı

### 1. Model Yüklendiğinde
```javascript
// ApsViewer.js - Model yüklendiğinde
viewer.addEventListener(Autodesk.Viewing.GEOMETRY_LOADED_EVENT, () => {
  extractModelInfo(); // Identity Data çıkarılır
});
```

### 2. Identity Data Çıkarma
```javascript
// Her element için Identity Data alanları taranır
const identityFields = [
  'Edited by', 'Alt Yüklenici', 'İşveren Hakediş No',
  'Alt Yüklenici Hakediş No', 'İmalat Tarihi', 'Activity ID',
  'İlerleme', 'Müşavir Onay Durumu'
];
```

### 3. AI ile İletişim
```javascript
// Doğal dil sorgusu analiz edilir
const toolSuggestion = mcpTools.suggestTool(userMessage);

// Uygun MCP tool çalıştırılır
const result = await mcpTools.executeTool(toolSuggestion.tool, ...args);
```

## 📝 API Endpoints

### `/api/ai/chat` (POST)
Ana AI chat endpoint'i. Identity Data sorularını işler.

**Request Body:**
```json
{
  "message": "Bu eleman hangi alt yüklenici tarafından yapılmış?",
  "modelId": "local-model",
  "aiModel": "deepseek/deepseek-chat"
}
```

**Response:**
```json
{
  "type": "text",
  "message": "Bu element XYZ İnşaat tarafından yapılmış. İlerleme durumu %75, müşavir onay durumu: Onaylandı."
}
```

### `/api/ai/modelInfo` (POST)
Model ve Identity Data bilgilerini günceller.

**Request Body:**
```json
{
  "modelInfo": {
    "name": "Proje Modeli",
    "categories": {...},
    "identityData": {
      "123": {
        "name": "Duvar-01",
        "category": "Walls",
        "identityData": {
          "Alt Yüklenici": "XYZ İnşaat",
          "İlerleme": "%75"
        }
      }
    }
  }
}
```

## 🎯 Örnek Kullanım Senaryoları

### Senaryo 1: Proje İlerleme Kontrolü
```
Kullanıcı: "Proje yüzde kaç tamamlandı?"
AI: "Proje ilerleme analizi:
- %100 Tamamlanan: 45 element
- %75 İlerlemede: 20 element  
- %50 İlerlemede: 15 element
- %25 İlerlemede: 8 element
- %0 Başlanmamış: 12 element

Genel ilerleme durumu %73 seviyesinde."
```

### Senaryo 2: Alt Yüklenici Analizi
```
Kullanıcı: "XYZ İnşaat kaç tane iş yapmış?"
AI: "XYZ İnşaat için 45 element bulundu.

Detaylar:
1. Duvar-01 (Walls) - İlerleme: %100 - Onay: Onaylandı
2. Duvar-02 (Walls) - İlerleme: %75 - Onay: Beklemede
3. Pencere-01 (Windows) - İlerleme: %100 - Onay: Onaylandı
... ve 42 element daha"
```

### Senaryo 3: Onay Durumu Kontrolü
```
Kullanıcı: "Hangi işler onay bekliyor?"
AI: "Müşavir onay durumu analizi:
- Onaylandı: 45 element
- Beklemede: 25 element
- Reddedildi: 5 element

Bekleyen elementleri vurgulamak ister misiniz?"
```

## 🔒 Güvenlik ve Performans

### Güvenlik
- Session-based authentication
- API key encryption
- Input validation
- Error handling

### Performans Optimizasyonu
- Memory cache for model data
- Lazy loading of Identity Data
- Streaming responses
- Timeout management (5s for model loading)

## 🛠️ Geliştirici Notları

### MCP Tools Genişletme
Yeni Identity Data fonksiyonu eklemek için:

1. **Function Definition:** `mcp-tools.js` içinde yeni fonksiyon tanımla
2. **Tool Registration:** `initializeTools()` içinde kaydet
3. **Natural Language:** `suggestTool()` içinde pattern matching ekle
4. **API Integration:** `routes/ai.js` içinde response handling ekle

### Debug Logging
Sistem kapsamlı debug logging sağlar:
```javascript
console.log('📋 MCP Tools: getElementIdentityData() çağrıldı');
console.log('🔍 ApsViewer: Extracting model information...');
console.log('🎯 AI Chat: Tool suggestion found:', toolSuggestion);
```

## 📈 Gelecek Geliştirmeler

### Planlanan Özellikler
- [ ] Zaman bazlı ilerleme analizi
- [ ] Malzeme ve maliyet entegrasyonu
- [ ] Risk analizi ve early warning system
- [ ] Otomatik rapor üretimi
- [ ] Multi-model comparison
- [ ] Real-time collaboration features

### API Genişletmeleri
- [ ] Batch Identity Data update
- [ ] Custom field definitions
- [ ] Export/Import functionality
- [ ] Webhook integrations

---

## 📞 Destek

Bu dokümantasyon 7Dimension MCP AI Server v2.0 için hazırlanmıştır.
Son güncellenme: 2024-12-18

**Teknik Destek:** development@7dimension.com
**Dokümantasyon:** docs.7dimension.com 

### 🎯 Dinamik Kategori Tanıma

Sistem, kullanıcının sözlü taleplerini otomatik olarak analiz ederek hangi kategorileri göstermek istediğini belirler:

**Akıllı Kategori Eşleme:**
- **Türkçe → İngilizce**: "duvar" → "wall", "çatı" → "roof", "kolon" → "column"
- **Esnek Arama**: "Revit Walls", "Revit Structural Columns", "Revit Windows" otomatik bulunur
- **Çoklu Dil Desteği**: "Show walls" veya "Duvarları göster" aynı sonucu verir
- **Çoklu Kategori**: "kapı ve pencere" → her iki kategoriyi de bulur ve gösterir

**Manuel Tanımlama YOK!** 
Sistem modelde hangi kategoriler varsa otomatik tanır. Yeni kategoriler eklendiğinde manuel kod yazmaya gerek yok.

**Desteklenen Kategori Türleri:**
- Duvarlar (Walls, Revit Walls, WALL, IfcWall)
- Pencereler (Windows, Revit Windows, WINDOW) 
- Kapılar (Doors, Revit Doors, DOOR)
- Kolonlar (Columns, Revit Structural Columns)
- Çatılar (Roofs, Revit Roofs)
- Döşemeler (Floors, Revit Floors, Slab)
- Tavanlar (Ceilings, Revit Ceilings)
- Merdivener (Stairs, Revit Stairs, Runs)
- Korkuluklar (Railings, Revit Railings)
- Kirişler (Framing, Revit Structural Framing)
- Mobilya (Furniture, Revit Furniture)
- Tesisat (Plumbing, Electrical, HVAC)
- **+ Modelde bulunan herhangi bir kategori** 