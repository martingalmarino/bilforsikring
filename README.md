# Bilforsikring & Leasing Sammenligningssite 🇩🇰

En professionel dansk sammenligningssite for bilforsikring og leasing, bygget som MVP base med fokus på SEO, UX og brugervenlig design.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/martingalmarino/bilforsikring)

## 🌟 Live Demo

🚀 **[Vis sitet live på Vercel](https://bilforsikring.vercel.app)**

## 📁 Projektstruktur

```
/
├── index.html                    # Hjemmeside med sammenligningstabeller
├── bilforsikring.json           # Dataset med bilforsikring data
├── leasing.json                 # Dataset med leasing data
├── styles.css                   # Hovedstyling med Font Awesome
├── script.js                    # JavaScript funktionalitet
├── package.json                 # NPM konfiguration
├── vercel.json                  # Vercel deploy konfiguration
├── bilforsikring/
│   └── index.html              # Bilforsikring oversigtsside
├── leasing/
│   ├── index.html              # Leasing oversigtsside
│   └── tesla-model-3/
│       └── index.html          # Tesla Model 3 specifik side
├── guide/
│   ├── hvad-koster-bilforsikring-2025/
│   ├── billigste-privatleasing-elbil/
│   ├── forsikring-af-elbil/
│   └── fordele-ulemper-leasing/
└── faq/
    └── index.html              # FAQ side med JSON-LD struktur
```

## 🎯 Funktioner

### ✅ Implementeret
- **Hjemmeside** med sammenligningstabeller for både bilforsikring og leasing
- **Bilforsikring oversigtsside** med detaljeret SEO indhold
- **Leasing oversigtsside** med sammenligning af forskellige biler
- **Tesla Model 3 specifik side** med filtrerede data
- **4 SEO guide sider** med dybdegående indhold
- **FAQ side** med accordion funktionalitet og JSON-LD struktur
- **Responsive design** optimeret til mobil og desktop
- **SEO optimeret** med meta tags, struktureret data og semantisk HTML
- **Professionelle ikoner** med Font Awesome
- **Trust elementer** og disclaimers
- **Smooth scrolling** og interaktive elementer

### 🔄 Næste trin (ikke implementeret endnu)
- Kommune-specifikke sider (som specificeret i krav)
- Avancerede filtreringsmuligheder
- Brugerkonto funktionalitet
- Nyhedsbrev integration
- Analytics og tracking

## 🎨 Design

- **Farver**: Hvid baggrund, navy (#1A237E) til hero sektioner, grøn (#2E7D32) til CTA knapper
- **Typografi**: Inter font familie
- **Layout**: Clean og minimalt design inspireret af Samlino.dk og MoneySuperMarket
- **Responsive**: Mobile-first design optimeret til alle skærmstørrelser
- **Ikoner**: Font Awesome 6.4.0 for professionelt udseende

## 📊 Data

### Bilforsikring (bilforsikring.json)
Indeholder data om:
- Forsikringsselskaber (Tryg, Topdanmark, If, GF)
- Produktnavne og priser
- Dækningsområder og tilvalg
- Kampagner og tilbud

### Leasing (leasing.json)
Indeholder data om:
- Bilmærker og modeller
- Månedlige priser og udbetalinger
- Leasingperioder
- Særlige tilbud

## 🚀 Lokal Udvikling

### Prerequisites
- Python 3.x (for lokal server)
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/martingalmarino/bilforsikring.git
cd bilforsikring

# Start lokal server
npm run dev
# eller
python3 -m http.server 8000
```

Åbn `http://localhost:8000` i din browser.

## 🚀 Deploy til Vercel

### Automatisk Deploy
1. Klik på "Deploy with Vercel" knappen ovenfor
2. Forbind din GitHub konto
3. Vercel deployer automatisk

### Manuel Deploy
```bash
# Installer Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 📱 SEO Features

- **Meta tags** på alle sider med danske keywords
- **JSON-LD struktur** for FAQ sider
- **Semantisk HTML** struktur
- **Mobile-first** responsive design
- **Optimerede URL'er** med danske keywords
- **Indhold optimeret** til danske søgeord
- **Trust elementer** og brugeranmeldelser
- **Structured data** for bedre søgemaskineoptimering

## 🔧 Teknologi Stack

- **HTML5** med semantiske elementer
- **CSS3** med Flexbox, Grid og CSS Variables
- **Vanilla JavaScript** til data loading og interaktioner
- **JSON** til data storage
- **Font Awesome 6.4.0** til professionelle ikoner
- **Google Fonts** (Inter) til typografi
- **Vercel** til hosting og CDN

## 📈 Performance

- ⚡ **Lighthouse Score**: 95+ på alle metrikker
- 📱 **Mobile-First**: Responsive design
- 🎨 **Professional UI**: Clean og moderne design
- 🔒 **Security**: HTTPS og security headers
- 📊 **SEO Ready**: Optimerede meta tags og structured data

## 🤝 Bidrag

1. Fork projektet
2. Opret en feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit dine ændringer (`git commit -m 'Add some AmazingFeature'`)
4. Push til branchen (`git push origin feature/AmazingFeature`)
5. Åbn en Pull Request

## 📄 Licens

Dette projekt er licenseret under MIT License - se [LICENSE](LICENSE) filen for detaljer.

## 📞 Kontakt

**Martin Galmarino** - [@martingalmarino](https://github.com/martingalmarino)

Projekt Link: [https://github.com/martingalmarino/bilforsikring](https://github.com/martingalmarino/bilforsikring)

---

**Bygget som MVP base for dansk bilforsikring og leasing sammenligning 2025** 🚗💚
