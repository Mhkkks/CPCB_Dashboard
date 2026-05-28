const form =
  document.getElementById(
    "uploadForm"
  );

const output =
  document.getElementById(
    "output"
  );

const sampleBtn =
  document.getElementById(
    "sampleBtn"
  );

const aqiContainer =
  document.getElementById(
    "aqiContainer"
  );

// =====================================
// AQI API
// =====================================

async function fetchAQI(city) {

  try {

    const token =
      "3e09b4eb66ea1f97a6beeb05afdb0f18add0173a";

    const response =
      await fetch(

        `https://api.waqi.info/feed/${city}/?token=${token}`
      );

    const data =
      await response.json();

    const aqi =
      data.data.aqi;

    let category = "";

    if (aqi <= 50) {

      category = "Good";

    } else if (aqi <= 100) {

      category = "Satisfactory";

    } else if (aqi <= 200) {

      category = "Moderate";

    } else if (aqi <= 300) {

      category = "Poor";

    } else if (aqi <= 400) {

      category = "Very Poor";

    } else {

      category = "Severe";
    }

    return `

      <div class="aqi-card">

        <h2>

          ${city.toUpperCase()}

        </h2>

        <div class="aqi-value">

          ${aqi}

        </div>

        <div class="aqi-category">

          ${category}

        </div>

        <p>

          Updated:
          ${data.data.time.s}

        </p>

      </div>
    `;

  } catch {

    return `

      <div class="aqi-card">

        AQI unavailable

      </div>
    `;
  }
}

// =====================================
// LOAD AQI
// =====================================

async function loadAQI() {

  const delhiAQI =
    await fetchAQI("delhi");

  const jodhpurAQI =
    await fetchAQI("jodhpur");

  aqiContainer.innerHTML = `

    <div class="aqi-grid">

      ${delhiAQI}

      ${jodhpurAQI}

    </div>
  `;
}

// =====================================
// INITIAL AQI
// =====================================

window.addEventListener(

  "load",

  async () => {

    await loadAQI();
  }
);

// =====================================
// AUTO REFRESH AQI
// =====================================

setInterval(

  async () => {

    await loadAQI();

  },

  3600000
);

// =====================================
// FORM SUBMIT
// =====================================

form.addEventListener(

  "submit",

  async (e) => {

    e.preventDefault();

    const formData =
      new FormData(form);

    output.innerHTML = `

      <div class="loading">

        Running Analysis...

      </div>
    `;

    try {

      const response =
        await fetch(

          "http://127.0.0.1:8000/run-analysis",

          {
            method: "POST",

            body: formData,
          }
        );

      const data =
        await response.json();

      await renderDashboard(data);

    } catch (error) {

      console.error(error);

      output.innerHTML = `

        <div class="error">

          Analysis Failed

        </div>
      `;
    }
  }
);

// =====================================
// SAMPLE DATASET
// =====================================

sampleBtn.addEventListener(

  "click",

  async () => {

    output.innerHTML = `

      <div class="loading">

        Running Sample Dataset...

      </div>
    `;

    try {

      const formData =
        new FormData();

      const files = [

        {
          key: "place1_2018",
          path:
          "./sample-data/delhi2019.xlsx"
        },

        {
          key: "place1_2023",
          path:
          "./sample-data/delhi2023.xlsx"
        },

        {
          key: "place2_2018",
          path:
          "./sample-data/jodhpur2019.xlsx"
        },

        {
          key: "place2_2023",
          path:
          "./sample-data/jodhpur2023.xlsx"
        }
      ];

      for (const file of files) {

        const response =
          await fetch(file.path);

        const blob =
          await response.blob();

        formData.append(
          file.key,
          blob,
          file.path.split("/").pop()
        );
      }

      const response =
        await fetch(

          "http://127.0.0.1:8000/run-analysis",

          {
            method: "POST",

            body: formData,
          }
        );

      const data =
        await response.json();

      await renderDashboard(data);

    } catch (error) {

      console.error(error);

      output.innerHTML = `

        <div class="error">

          Sample Dataset Failed

        </div>
      `;
    }
  }
);

// =====================================
// RENDER DASHBOARD
// =====================================

async function renderDashboard(data) {

  output.innerHTML = `

    <div class="results-grid">

      ${createCard(

        "Place 1 PM2.5 Histograms",

        data.place1_results
        .pm25_histograms.plot_url
      )}

      ${createCard(

        "Place 1 Heat Index Histograms",

        data.place1_results
        .hi_histograms.plot_url
      )}

      ${createCard(

        "Place 1 Double Diurnal Curves",

        data.place1_results
        .double_diurnal_curves
      )}

      ${createCard(

        "Place 1 Correlation Analysis",

        data.place1_results
        .correlation_analysis
      )}

      ${createCard(

        "Place 2 PM2.5 Histograms",

        data.place2_results
        .pm25_histograms.plot_url
      )}

      ${createCard(

        "Place 2 Heat Index Histograms",

        data.place2_results
        .hi_histograms.plot_url
      )}

      ${createCard(

        "Place 2 Double Diurnal Curves",

        data.place2_results
        .double_diurnal_curves
      )}

      ${createCard(

        "Place 2 Correlation Analysis",

        data.place2_results
        .correlation_analysis
      )}

    </div>
  `;
}

// =====================================
// GRAPH CARD
// =====================================

function createCard(
  title,
  imageUrl
) {

  return `

    <div class="graph-card">

      <h3>

        ${title}

      </h3>

      <img
        src="${imageUrl}"
        onclick="window.open('${imageUrl}', '_blank')"
      />

    </div>
  `;
}