const form = document.getElementById(
  "uploadForm"
);

const output = document.getElementById(
  "output"
);

form.addEventListener(

  "submit",

  async (e) => {

    e.preventDefault();

    const formData = new FormData(form);

    output.innerHTML =
      "<h2>Generating graphs...</h2>";

    try {

      const response = await fetch(

        "http://127.0.0.1:8000/run-analysis",

        {
          method: "POST",

          body: formData,
        }
      );

      const data =
        await response.json();

      console.log(data);

      output.innerHTML = `

        <div class="results-grid">

          <!-- PLACE 1 -->

          <div class="graph-card">

            <h3>
              Place 1 - PM2.5
            </h3>

            <img
              src="${data.place1_results.pm25_histograms.plot_url}"
            />
          </div>

          <div class="graph-card">

            <h3>
              Place 1 - Heat Index
            </h3>

            <img
              src="${data.place1_results.hi_histograms.plot_url}"
            />
          </div>

          <div class="graph-card">

            <h3>
              Place 1 - Diurnal
            </h3>

            <img
              src="${data.place1_results.double_diurnal_curves}"
            />
          </div>

          <div class="graph-card">

            <h3>
              Place 1 - Correlation
            </h3>

            <img
              src="${data.place1_results.correlation_analysis}"
            />
          </div>

          <!-- PLACE 2 -->

          <div class="graph-card">

            <h3>
              Place 2 - PM2.5
            </h3>

            <img
              src="${data.place2_results.pm25_histograms.plot_url}"
            />
          </div>

          <div class="graph-card">

            <h3>
              Place 2 - Heat Index
            </h3>

            <img
              src="${data.place2_results.hi_histograms.plot_url}"
            />
          </div>

          <div class="graph-card">

            <h3>
              Place 2 - Diurnal
            </h3>

            <img
              src="${data.place2_results.double_diurnal_curves}"
            />
          </div>

          <div class="graph-card">

            <h3>
              Place 2 - Correlation
            </h3>

            <img
              src="${data.place2_results.correlation_analysis}"
            />
          </div>

        </div>
      `;

    } catch (error) {

      console.error(error);

      output.innerHTML = `

        <div style="
          color:red;
          font-size:20px;
          margin-top:20px;
        ">

          Analysis failed

        </div>
      `;
    }
  }
);