document.addEventListener("DOMContentLoaded", () => {
    const navButtons = document.querySelectorAll(".nav_btn");
    const windows = document.querySelectorAll(".window");

    function activateTab(tabId) {
        windows.forEach(win => {
            if (win.id === tabId) win.classList.add("active");
            else win.classList.remove("active");
        });
    }
    activateTab("strategy_window");

    navButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetTabId = button.getAttribute("data-tab");
            if (targetTabId) activateTab(targetTabId);
        });
    
    const runTyresBtn = document.getElementById("run_tyres_analyse");
    const trackTyresSelect = document.getElementById("track_input_tyres");

    runTyresBtn.addEventListener("click", async () => {
        const selectedTrack = trackTyresSelect.value;

        runTyresBtn.innerText = "Анализируем...";
        runTyresBtn.disabled = true;

        try {
            const response = await fetch(`http://localhost:8080/api/predict?track=${encodeURIComponent(selectedTrack)}&safety=2`);
            const data = await response.json();

            if (data.status === "success") {
                document.getElementById("tyres_annotation").innerText = `Ресурс шин для ${selectedTrack}:`;

                document.getElementById("soft_tyre_res_km").innerText = `${Math.round(data.tyre_laps.SOFT * data.lap_len)} км`;
                document.getElementById("soft_tyre_res_laps").innerText = `${data.tyre_laps.SOFT} кругов`;
                
                document.getElementById("medium_tyre_res_km").innerText = `${Math.round(data.tyre_laps.MEDIUM * data.lap_len)} км`;
                document.getElementById("medium_tyre_res_laps").innerText = `${data.tyre_laps.MEDIUM} кругов`;
                
                document.getElementById("hard_tyre_res_km").innerText = `${Math.round(data.tyre_laps.HARD * data.lap_len)} км`;
                document.getElementById("hard_tyre_res_laps").innerText = `${data.tyre_laps.HARD} кругов`;
            } else {
                alert("Ошибка бэкенда: " + data.message);
            }
        } catch (err) {
            alert("Не удалось подключиться: " + err);
        } finally {
            runTyresBtn.innerText = "Анализ ресурса шин";
            runTyresBtn.disabled = false;
        }
    });

    });

    const runBtn = document.getElementById("run_strategy");
    const trackSelect = document.getElementById("track_input_strategy");
    const safetySlider = document.getElementById("input_safety_reserve");
    const strategiesList = document.getElementById("strategies_list");
    const trackHeader = document.querySelector("#strategy_output header");

    runBtn.addEventListener("click", async () => {
        const selectedTrack = trackSelect.value;
        const safetyValue = safetySlider.value;

        runBtn.innerText = "Расчитываем варианты...";
        runBtn.disabled = true;

        try {
            const response = await fetch(`http://localhost:8080/api/predict?track=${encodeURIComponent(selectedTrack)}&safety=${safetyValue}`);
            const data = await response.json();

            if (data.status === "success") {
                trackHeader.innerText = `--- ${selectedTrack.toUpperCase()} (${data.laps_total} КРУГОВ, ${data.lap_len} KM) ---`;
                
                const infoBox = document.querySelector("#strategy_output details article");
                infoBox.innerHTML = `
                    <div style="display: flex; gap: 20px; align-items: center;">
                
                        <p><strong>Страна проведения:</strong> ${data.country}</p>
                        <p><strong>Дистанция гонки:</strong> Круги: ${data.laps_total}; Км: ${Math.round(data.laps_total * data.lap_len)}</p>
                        <p><strong>Климатические условия:</strong> ${data.climate}</p>
                        <p><strong>Степень абразивности асфальта:</strong> ${data.asphalt}</p>
                        
                    </div>
                `;
                strategiesList.innerHTML = "";

                data.strategies.forEach((strat, index) => {
                    const li = document.createElement("li");
                    li.className = "strategy_variant";
                    
                    const chainText = strat.chain.join(" ➔ ");
                    
                    let lineHtml = '<div class="strategy_line">';
                    let currentLap = 1;

                    strat.pits.forEach((pitLap, idx) => {
                        const stintLaps = pitLap - currentLap;
                        const tyreType = strat.chain[idx].toLowerCase();
                        lineHtml += `<div class="stint_segment ${tyreType}" style="flex-grow: ${stintLaps};" title="Stint ${idx+1}: ${strat.chain[idx]}">${strat.chain[idx]}</div>`;
                        
                        const currentTyre = strat.chain[idx].toLowerCase();
                        const nextTyre = strat.chain[idx + 1].toLowerCase();
                        
                        const transitionClass = `${currentTyre}-${nextTyre}`;
                        
                        lineHtml += `<div class="stint_segment pit_window_segment ${transitionClass}" style="flex-grow: 5;" title="Pit Window (Laps ${pitLap-3}-${pitLap+2})"></div>`;
                        currentLap = pitLap + 5;
                    });

                    
                    const finalLaps = data.laps_total - currentLap;
                    const finalTyre = strat.chain[strat.chain.length - 1].toLowerCase();
                    if (finalLaps > 0) {
                        lineHtml += `<div class="stint_segment ${finalTyre}" style="flex-grow: ${finalLaps};" title="Final Stint: ${strat.chain[strat.chain.length - 1]}">${strat.chain[strat.chain.length - 1][0]}</div>`;
                    }
                    lineHtml += '</div>';

                    const pitStrings = strat.pits.map(p => `Круг ${p} (окно: ${p-3}-${p+2})`);
                    const pitInfo = pitStrings.length ? pitStrings.join(", ") : "Нет пит-стопов";

                    li.innerHTML = `
                        <h3 class="strategy_name">${chainText}</h3>
                        ${lineHtml}
                        <p class="pitstop_description">Окна пит-стопов: ${pitInfo} | Индекс безопасности: +${strat.safety} кругов в резерве</p>
                    `;
                    strategiesList.appendChild(li);
                });

                document.getElementById("soft_tyre_res_km").innerText = `${Math.round(data.tyre_laps.SOFT * data.lap_len)} км`;
                document.getElementById("soft_tyre_res_laps").innerText = `${data.tyre_laps.SOFT} кругов`;
                
                document.getElementById("medium_tyre_res_km").innerText = `${Math.round(data.tyre_laps.MEDIUM * data.lap_len)} км`;
                document.getElementById("medium_tyre_res_laps").innerText = `${data.tyre_laps.MEDIUM} кругов`;
                
                document.getElementById("hard_tyre_res_km").innerText = `${Math.round(data.tyre_laps.HARD * data.lap_len)} км`;
                document.getElementById("hard_tyre_res_laps").innerText = `${data.tyre_laps.HARD} кругов`;
            } else {
                alert("Ошибка бэкенда: " + data.message);
            }
                const moreBtn = document.getElementById("more_strategy");
                const allRenderedStrats = strategiesList.querySelectorAll(".strategy_variant");

                if (allRenderedStrats.length <= 3) {
                    moreBtn.style.display = "none";
                } else {
                    moreBtn.style.display = "block";
                    moreBtn.innerText = "▼ Показать альтернативные стратегии";
                    
                    allRenderedStrats.forEach((strat, idx) => {
                        if (idx > 2) strat.classList.add("hidden_strat");
                    });
                }

                moreBtn.onclick = () => {
                    const hiddenStrats = strategiesList.querySelectorAll(".strategy_variant.hidden_strat");
                    
                    if (hiddenStrats.length > 0) {
                        hiddenStrats.forEach(strat => strat.classList.remove("hidden_strat"));
                        moreBtn.innerText = "▲ Спрятать альтернативные стратегии";
                    } else {
                        allRenderedStrats.forEach((strat, idx) => {
                            if (idx > 2) strat.classList.add("hidden_strat");
                        });
                        moreBtn.innerText = "▼ Показать альтернативные стратегии";
                    }
                };


        } catch (err) {
            alert("Не удалось подключиться к Python-серверу: " + err);
        } finally {
            runBtn.innerText = "Получить стратегии";
            runBtn.disabled = false;
        }
    });
});