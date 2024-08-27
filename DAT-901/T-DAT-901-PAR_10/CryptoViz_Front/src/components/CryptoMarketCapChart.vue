<template>
    <div id="chartdiv" ref="chartdiv" style="width: 100%; height: 500px;" align-content-center></div>
  </template>
  
  <script>
  import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
  export default {
    name: 'CryptoMarketCapChart',
    props: {
      chartData: {
        type: Array,
      },
    },
    watch: {
    chartData() {
      if (this.root) {
        this.root.dispose(); // Dispose de l'ancien graphique
      }
      this.$nextTick(() => {
        this.initChart(); // Initialise le nouveau graphique avec les données mises à jour
      });
    }
  },
    mounted() {
      this.initChart();
    },
    beforeUnmount() {
      if (this.chart) {
        this.root.dispose();
      }
    },
    methods: {
      initChart() {
        const am5 = require("@amcharts/amcharts5");
        const am5hierarchy = require("@amcharts/amcharts5/hierarchy");
  
        const root = am5.Root.new(this.$refs.chartdiv);
  
        root.setThemes([am5themes_Animated.new(root)]);
  
        const container = root.container.children.push(am5.Container.new(root, {
          width: am5.percent(200),
          height: am5.percent(100),
          layout: root.verticalLayout
        }));
  
        const series = container.children.push(am5hierarchy.Treemap.new(root, {
          singleBranchOnly: false,
          downDepth: 1,
          upDepth: -1,
          initialDepth: 2,
          valueField: "value",
          categoryField: "name",
          childDataField: "children",
          nodePaddingOuter: 1,
          nodePaddingInner: 0
        }));
  
        series.labels.template.setAll({
  text: "{fullname} ({category})\n{current_price}$\n{marketCapChangePercentage24h}%",
  fontSize: 20,
  fill: am5.color(0xffffff),
  textAlign: "center", // Cette ligne aligne le texte au centre
  centerY: am5.percent(50), // Centre verticalement le texte dans le noeud
  centerX: am5.percent(50)  // Centre horizontalement le texte dans le noeud
});


        series.rectangles.template.setAll({
          strokeWidth: 2
        });

        // Lors du survol, changer la couleur du contour
series.rectangles.template.events.on("pointerover", function(ev) {
  ev.target.set("stroke", am5.color(0x3C48B4)); // Couleur de contour au survol
  ev.target.set("strokeWidth", 2); // Optionnel : Augmenter l'épaisseur du contour au survol
});

// Lors de la sortie du survol, restaurer la couleur du contour originale
series.rectangles.template.events.on("pointerout", function(ev) {
  ev.target.set("stroke", am5.color(0xffffff)); // Restaurer la couleur de contour initiale
  ev.target.set("strokeWidth", 2); // Optionnel : Restaurer l'épaisseur du contour initiale
});


        series.rectangles.template.adapters.add("fill", function(fill, target) {
  const changePercentage = target.dataItem.dataContext.marketCapChangePercentage24h;
  if (changePercentage >= 5) {
    return am5.color(0x008000); // Vert très foncé
  } else if (changePercentage > 0) {
    return am5.color(0x50b300); // Vert
  } else if (changePercentage <= -5) {
    return am5.color(0x8b0000); // Rouge très foncé
  } else if (changePercentage < 0) {
    return am5.color(0xb30000); // Rouge
  } else {
    return am5.color(0x808080); // Gris pour 0%
  }
});

const vm = this; // Capturez le contexte Vue pour l'utiliser dans la fonction de callback

series.rectangles.template.events.on("click", function(ev) {
  let cryptoId = ev.target.dataItem.dataContext.cryptoId; // Obtenez l'ID de la crypto

  // Naviguez vers la vue détaillée de la crypto en utilisant $router.push
  console.log(cryptoId);
  vm.$router.push({ name: 'CryptoView', params: { id: cryptoId } });
});

        
  
        // Utilisez les props pour les données si vous voulez les rendre dynamiques
        series.data.setAll(this.chartData);
  
        series.set("selectedDataItem", series.dataItems[0]);
  
        series.appear(1000, 100);
  
        this.root = root;
      }
    }
  };
  </script>
  