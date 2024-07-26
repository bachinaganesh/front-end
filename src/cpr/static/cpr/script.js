document.addEventListener("DOMContentLoaded", function() {
    var checkbox = document.querySelector("#id_conditional_trade");
    var onLong = document.querySelector(".onlong");
    var onShort = document.querySelector(".onshort");
    var onLongSignal = document.querySelector("#id_onlongsignal");
    var onShortSignal = document.querySelector("#id_onshortsignal");
    var onLongStrikeSelection = document.querySelector("#id_onlongstrikeselection");
    var onShortStrikeSelection = document.querySelector("#id_onshortstrikeselection");
    var dynamicFieldsLongContainer = document.querySelector("#dynamic_long_container");
    var dynamicFieldsShortContainer = document.querySelector("#dynamic_short_container");
    var exitType = document.querySelector("#id_exit_type");
    var exitTypeFields = document.querySelector(".exit_type_fields");
    var trailingType = document.querySelector("#id_trailing_type");
    var trailingTypeFields = document.querySelector(".trailing_type_fields");

    updateTrailingTypeFields();
    trailingType.addEventListener("change", updateTrailingTypeFields);

    function updateTrailingTypeFields() {
        trailingTypeFields.innerHTML = "";

        var x_field_container = document.createElement("div");
        x_field_container.id = "x_field";

        var y_field_container = document.createElement('div');
        y_field_container.id = "y_field";

        // x fields
        const xLabel = document.createElement('label');
        xLabel.textContent = "X";
        x_field_container.appendChild(xLabel);

        const xValue = document.createElement('input');
        xValue.type = "number";
        xValue.name = "x";
        x_field_container.appendChild(xValue);

        const xCheckBoxLabel = document.createElement('label');
        xCheckBoxLabel.textContent = " Optimize:";
        x_field_container.appendChild(xCheckBoxLabel);

        const xCheckBox = document.createElement('input');
        xCheckBox.type = "checkbox";
        xCheckBox.name = "x_optimize";
        xCheckBox.disabled=true;
        x_field_container.appendChild(xCheckBox);

        const xMinLabel = document.createElement('label');
        xMinLabel.textContent = "Min";
        x_field_container.appendChild(xMinLabel);
        xMinLabel.style.display = "none";

        const xMinField = document.createElement('input');
        xMinField.type = "number";
        xMinField.name = "x_min_field";
        x_field_container.appendChild(xMinField);
        xMinField.style.display = "none";

        const xMaxLabel = document.createElement('label');
        xMaxLabel.textContent = "Max";
        x_field_container.appendChild(xMaxLabel);
        xMaxLabel.style.display = "none";

        const xMaxField = document.createElement('input');
        xMaxField.type = "number";
        xMaxField.name = "x_max_field";
        x_field_container.appendChild(xMaxField);
        xMaxField.style.display = "none";

        const xStepLabel = document.createElement('label');
        xStepLabel.textContent = "Step";
        x_field_container.appendChild(xStepLabel);
        xStepLabel.style.display = "none";

        const xStepField = document.createElement("input");
        xStepField.type = "number";
        xStepField.name = "x_step_field";
        x_field_container.appendChild(xStepField);
        xStepField.style.display = "none";

        // xCheckBox.addEventListener("change", function() {
        //     if(this.checked) {
        //         xMinLabel.style.display = "inline-block";
        //         xMaxLabel.style.display = "inline-block";
        //         xStepLabel.style.display = "inline-block";
        //         xMinField.style.display = "inline-block";
        //         xMaxField.style.display = "inline-block";
        //         xStepField.style.display = "inline-block";
        //     }
        //     else {
        //         xMinLabel.style.display = "none";
        //         xMaxLabel.style.display = "none";
        //         xStepLabel.style.display = "none";
        //         xMinField.style.display = "none";
        //         xMaxField.style.display = "none";
        //         xStepField.style.display = "none";
        //     }
        // })


        // y fields
        const yLabel = document.createElement('label');
        yLabel.textContent = "Y";
        y_field_container.appendChild(yLabel);

        const yValue = document.createElement('input');
        yValue.type = "number";
        yValue.name = "y";
        y_field_container.appendChild(yValue);

        const yCheckBoxLabel = document.createElement('label');
        yCheckBoxLabel.textContent = " Optimize:";
        y_field_container.appendChild(yCheckBoxLabel);

        const yCheckBox = document.createElement('input');
        yCheckBox.type = "checkbox";
        yCheckBox.name = "y_optimize";
        yCheckBox.disabled = true;
        y_field_container.appendChild(yCheckBox);

        const yMinLabel = document.createElement('label');
        yMinLabel.textContent = "Min";
        y_field_container.appendChild(yMinLabel);
        yMinLabel.style.display = "none";

        const yMinField = document.createElement('input');
        yMinField.type = "number";
        yMinField.name = "y_min_field";
        y_field_container.appendChild(yMinField);
        yMinField.style.display = "none";

        const yMaxLabel = document.createElement('label');
        yMaxLabel.textContent = "Max";
        y_field_container.appendChild(yMaxLabel);
        yMaxLabel.style.display = "none";

        const yMaxField = document.createElement('input');
        yMaxField.type = "number";
        yMaxField.name = "y_max_field";
        y_field_container.appendChild(yMaxField);
        yMaxField.style.display = "none";

        const yStepLabel = document.createElement('label');
        yStepLabel.textContent = "Step";
        y_field_container.appendChild(yStepLabel);
        yStepLabel.style.display = "none";

        const yStepField = document.createElement("input");
        yStepField.type = "number";
        yStepField.name = "y_step_field";
        y_field_container.appendChild(yStepField);
        yStepField.style.display = "none";

        // yCheckBox.addEventListener("change", function() {
        //     if(this.checked) {
        //         yMinLabel.style.display = "inline-block";
        //         yMaxLabel.style.display = "inline-block";
        //         yStepLabel.style.display = "inline-block";
        //         yMinField.style.display = "inline-block";
        //         yMaxField.style.display = "inline-block";
        //         yStepField.style.display = "inline-block";
        //     }
        //     else {
        //         yMinLabel.style.display = "none";
        //         yMaxLabel.style.display = "none";
        //         yStepLabel.style.display = "none";
        //         yMinField.style.display = "none";
        //         yMaxField.style.display = "none";
        //         yStepField.style.display = "none";
        //     }
        // })

        trailingTypeFields.appendChild(x_field_container);
        trailingTypeFields.appendChild(y_field_container);

    }


    updateExitTimeFields();
    exitType.addEventListener("change", updateExitTimeFields);

    function updateExitTimeFields() {
        if(exitType.value === "time price") {
            exitTypeFields.innerHTML = '';
            var field_container = document.createElement("div");
            field_container.id = "field";
            const exitTimeLabel = document.createElement('label');
            exitTimeLabel.textContent = "Exit Time ";
            field_container.appendChild(exitTimeLabel);

            const exitTime = document.createElement("input");
            exitTime.type = "time";
            exitTime.name = "exit_time";
            field_container.appendChild(exitTime);

            const exitTimeCheckBoxLabel = document.createElement('label');
            exitTimeCheckBoxLabel.textContent = " Optimize:";
            field_container.appendChild(exitTimeCheckBoxLabel);

            const exitTimeCheckBox = document.createElement('input');
            exitTimeCheckBox.type = "checkbox";
            exitTimeCheckBox.name = "exit_time_optimize";
            exitTimeCheckBox.disabled = true;
            field_container.appendChild(exitTimeCheckBox);

            const exitMinLabel = document.createElement('label');
            exitMinLabel.textContent = "Min";
            field_container.appendChild(exitMinLabel);
            exitMinLabel.style.display = "none";

            const exitMinField = document.createElement('input');
            exitMinField.type = "number";
            exitMinField.name = "exit_min_field";
            field_container.appendChild(exitMinField);
            exitMinField.style.display = "none";
            
            const exitMaxLabel = document.createElement('label');
            exitMaxLabel.textContent = "Max";
            field_container.appendChild(exitMaxLabel);
            exitMaxLabel.style.display = "none";

            const exitMaxField = document.createElement('input');
            exitMaxField.type = "number";
            exitMaxField.name = "exit_max_field";
            field_container.appendChild(exitMaxField);
            exitMaxField.style.display = "none";

            const exitStepLabel = document.createElement('label');
            exitStepLabel.textContent = "Step";
            field_container.appendChild(exitStepLabel);
            exitStepLabel.style.display = "none";

            const exitStepField = document.createElement("input");
            exitStepField.type = "number";
            exitStepField.name = "exit_step_field";
            field_container.appendChild(exitStepField);
            exitStepField.style.display = "none";

            // exitTimeCheckBox.addEventListener("change", function() {
            //     if(this.checked) {
            //         exitMinLabel.style.display = "inline-block";
            //         exitMaxLabel.style.display = "inline-block";
            //         exitStepLabel.style.display = "inline-block";
            //         exitMinField.style.display = "inline-block";
            //         exitMaxField.style.display = "inline-block";
            //         exitStepField.style.display = "inline-block";
            //     }
            //     else {
            //         exitMinLabel.style.display = "none";
            //         exitMaxLabel.style.display = "none";
            //         exitStepLabel.style.display = "none";
            //         exitMinField.style.display = "none";
            //         exitMaxField.style.display = "none";
            //         exitStepField.style.display = "none";
            //     }
            // })
            exitTypeFields.appendChild(field_container);
        }
        else {
            exitTypeFields.innerHTML = '';
        }
    }

    // CPR Fields
    var cprOptimizeCheckBox = document.querySelector("#id_cpr_optimize");
    var cprOptimizeFields = document.querySelector(".cpr_optimize_fields");

    onLong.style.display = "none";
    onShort.style.display = "none";
    cprOptimizeFields.style.display = "none";

    // logic for to show on_long and on_short fields initially
    checkbox.addEventListener("change", function() {
        if (checkbox.checked) {
            onLong.style.display = "block";
            onShort.style.display = "block";
            updateLongFields();
            updateShortFields();
        } else {
            onLong.style.display = "none";
            onShort.style.display = "none";
        }
        
    });

    // logic for cpr optimize checkbox
    cprOptimizeCheckBox.addEventListener("change", function() {
        if(cprOptimizeCheckBox.checked) {
            cprOptimizeFields.style.display = "inline-block";
        }
        else {
            cprOptimizeFields.style.display = "none";
        }
    })

    onLongSignal.addEventListener("change", updateLongFields);
    onLongStrikeSelection.addEventListener("change", updateLongFields);

    onShortSignal.addEventListener("change", updateShortFields);
    onShortStrikeSelection.addEventListener("change", updateShortFields);

    var greeksChoices = ["!=", ">=", "<="];
    var greeksNames = ["delta", "gama", "vega", "theta"]

    // update long fields
    function updateLongFields() {
        var longSignalValue = onLongSignal.value;
        var longStrikeValue = onLongStrikeSelection.value;
        dynamicFieldsLongContainer.innerHTML = '';

        let numberOfFields = 0;
        let fieldNamePrefix = '';

        // logic for to get number of fields add dynamically 
        if(longSignalValue === "long call") {
            numberOfFields = 1;
        }
        else if(longSignalValue === "short call") {
            numberOfFields = 1;
        }
        else if(longSignalValue === "long put") {
            numberOfFields = 1;
        }
        else if(longSignalValue === "short put") {
            numberOfFields = 1;
        }
        else {
            numberOfFields = 0;
        }

        var longChoices = ["!=", ">=", "<="];
        // logic for getting prefix name
        if(longStrikeValue === "premium") {
            fieldNamePrefix = "premium_long";
        }
        else if(longStrikeValue === "atm") {
            fieldNamePrefix = "atm_long";
            longChoices = [];
            for(let i=-10; i<=10; i++) {
                longChoices.push(i);
            }
        }
        else if(longStrikeValue === "greeks") {
            fieldNamePrefix = "greeks_long";
        }

        // adding fields based on number_of_fields value
        for(let i=0; i<numberOfFields; i++) {
            if(longStrikeValue!="greeks")
            {
                const fieldContainer = document.createElement("div");
                fieldContainer.id = "field_container";

                const fieldLabel = document.createElement('label');
                fieldLabel.textContent = `${fieldNamePrefix}_${i+1}`;
                fieldContainer.appendChild(fieldLabel);

                const choiceField = document.createElement('select');
                choiceField.name = `choice_${fieldNamePrefix}_${i+1}`;
                longChoices.forEach(choice=> {
                    const option = document.createElement('option');
                    option.value = choice;
                    option.textContent = choice;
                    if(longStrikeValue === "atm" && choice == 0) {
                        option.selected = true;
                    }
                    choiceField.append(option);
                });
                fieldContainer.appendChild(choiceField);
                
                const fieldInput = document.createElement('input');
                fieldInput.type = "text";
                fieldInput.name = `input_${fieldNamePrefix}_${i+1}`;
                fieldInput.placeholder = `Enter ${fieldNamePrefix} Value ${i+1}`;
                fieldContainer.appendChild(fieldInput);

                const optimizeCheckBox = document.createElement('input');
                optimizeCheckBox.type = "checkbox";
                optimizeCheckBox.name = `optimize_${fieldNamePrefix}_${i+1}`;
                optimizeCheckBox.disabled = true;
                fieldContainer.appendChild(optimizeCheckBox);


                const optimizeLabel = document.createElement('label');
                optimizeLabel.textContent = "Optimize";
                fieldContainer.appendChild(optimizeLabel);

                const maxLabel = document.createElement('label');
                maxLabel.textContent = "Max:";
                fieldContainer.appendChild(maxLabel);
                maxLabel.style.display = "none";

                const maxInput = document.createElement('input');
                maxInput.type = "text";
                maxInput.name = `max_${fieldNamePrefix}_${i+1}`;
                maxInput.placeholder = "Max Value";
                fieldContainer.appendChild(maxInput);
                maxInput.style.display = "none";

                const minLabel = document.createElement('label');
                minLabel.textContent = "Min:";
                fieldContainer.appendChild(minLabel);
                minLabel.style.display = "none";

                const minInput = document.createElement('input');
                minInput.type = "text";
                minInput.name = `min_${fieldNamePrefix}_${i+1}`;
                minInput.placeholder = "Min Value";
                fieldContainer.appendChild(minInput);
                minInput.style.display = "none";

                const stepLabel = document.createElement('label');
                stepLabel.textContent = "Step:";
                fieldContainer.appendChild(stepLabel);
                stepLabel.style.display = "none";

                const stepInput = document.createElement('input');
                stepInput.type = "text";
                stepInput.name = `step_${fieldNamePrefix}_${i+1}`;
                stepInput.placeholder = "Step Value";
                fieldContainer.appendChild(stepInput);
                stepInput.style.display = "none";

                // optimizeCheckBox.addEventListener("change", function() {
                //     if (this.checked) {
                //         maxInput.style.display = 'inline-block';
                //         minInput.style.display = 'inline-block';
                //         stepInput.style.display = 'inline-block';
                //         maxLabel.style.display = "inline-block";
                //         minLabel.style.display = "inline-block";
                //         stepLabel.style.display = "inline-block";
                //     } else {
                //         maxInput.style.display = 'none';
                //         minInput.style.display = 'none';
                //         stepInput.style.display = 'none';
                //         maxLabel.style.display = "none";
                //         minLabel.style.display = "none";
                //         stepLabel.style.display = "none";
                //     }
                // });
                dynamicFieldsLongContainer.appendChild(fieldContainer);
            }
            else {
                const outerContainer = document.createElement('div');
                outerContainer.id = "fields";
                for(let j=0; j<greeksNames.length; j++) {
                    const innerContainer = document.createElement('div');
                    innerContainer.id = "field_container";
                    const inputFieldLabel = document.createElement('label');
                    inputFieldLabel.textContent = `${greeksNames[j].toUpperCase()}_${i+1}`;
                    innerContainer.appendChild(inputFieldLabel);

                    const inputChoiceField = document.createElement('select');
                    inputChoiceField.name = `choice_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    greeksChoices.forEach(choice=> {
                        const option = document.createElement('option');
                        option.value = choice;
                        option.textContent = choice;
                        inputChoiceField.append(option);
                    });
                    innerContainer.appendChild(inputChoiceField);

                    const fieldInput = document.createElement('input');
                    fieldInput.type = "number";
                    fieldInput.placeholder = "Enter Delta Value";
                    fieldInput.name = `input_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    innerContainer.appendChild(fieldInput);

                    const optimizeCheckBox = document.createElement('input');
                    optimizeCheckBox.type = "checkbox";
                    optimizeCheckBox.name = `optimize_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    optimizeCheckBox.disabled = true;
                    innerContainer.appendChild(optimizeCheckBox);

                    const optimizeLabel = document.createElement('label');
                    optimizeLabel.textContent = "Optimize ";
                    innerContainer.appendChild(optimizeLabel);

                    const maxLabel = document.createElement('label');
                    maxLabel.textContent = "Max:";
                    innerContainer.appendChild(maxLabel);
                    maxLabel.style.display = "none";

                    const maxInput = document.createElement('input');
                    maxInput.type = "text";
                    maxInput.name = `max_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    maxInput.placeholder = "Max Value";
                    innerContainer.appendChild(maxInput);
                    maxInput.style.display = "none";

                    const minLabel = document.createElement('label');
                    minLabel.textContent = "Min:";
                    innerContainer.appendChild(minLabel);
                    minLabel.style.display = "none";

                    const minInput = document.createElement('input');
                    minInput.type = "text";
                    minInput.name = `min_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    minInput.placeholder = "Min Value";
                    innerContainer.appendChild(minInput);
                    minInput.style.display = "none";

                    const stepLabel = document.createElement('label');
                    stepLabel.textContent = "Step:";
                    innerContainer.appendChild(stepLabel);
                    stepLabel.style.display = "none";

                    const stepInput = document.createElement('input');
                    stepInput.type = "text";
                    stepInput.name = `step_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    stepInput.placeholder = "Step Value";
                    innerContainer.appendChild(stepInput);
                    stepInput.style.display = "none";

                    // optimizeCheckBox.addEventListener("change", function() {
                    //     if (this.checked) {
                    //         maxInput.style.display = 'inline-block';
                    //         minInput.style.display = 'inline-block';
                    //         stepInput.style.display = 'inline-block';
                    //         maxLabel.style.display = "inline-block";
                    //         minLabel.style.display = "inline-block";
                    //         stepLabel.style.display = "inline-block";
                    //     } else {
                    //         maxInput.style.display = 'none';
                    //         minInput.style.display = 'none';
                    //         stepInput.style.display = 'none';
                    //         maxLabel.style.display = "none";
                    //         minLabel.style.display = "none";
                    //         stepLabel.style.display = "none";
                    //     }
                    // });
                    outerContainer.appendChild(innerContainer);
                dynamicFieldsLongContainer.appendChild(outerContainer);
            }
        }  
    }
    }

    // function logic for on short dynamic adding fields
    function updateShortFields() {
        var shortSignalValue = onShortSignal.value;
        var shortStrikeValue = onShortStrikeSelection.value;
        dynamicFieldsShortContainer.innerHTML = '';

        let numberOfFields = 0;
        let fieldNamePrefix = '';
        var shortChoices = ["!=", ">=", "<="];
        if(shortSignalValue === "long put") {
            numberOfFields = 1;
        }
        else if(shortSignalValue === "short put") {
            numberOfFields = 1;
        }
        else if(shortSignalValue === "long call") {
            numberOfFields = 1;
        }
        else if(shortSignalValue === "short call") {
            numberOfFields = 1;
        }
        else {
            numberOfFields = 0;
        }

        if(shortStrikeValue === "premium") {
            fieldNamePrefix = "premium_short";
        }
        else if(shortStrikeValue === "atm") {
            fieldNamePrefix = "atm_short";
            shortChoices = [];
            for(let i=-10; i<=10; i++) {
                shortChoices.push(i);
            }
        }
        else if(shortStrikeValue === "greeks") {
            fieldNamePrefix = "greeks_short";
        }

        for(let i=0; i<numberOfFields; i++) {
            if(shortStrikeValue!="greeks") {
            const fieldContainer = document.createElement("div");
            fieldContainer.id = "field_container";

            const fieldLabel = document.createElement('label');
            fieldLabel.textContent = `${fieldNamePrefix}_${i+1}`;
            fieldContainer.appendChild(fieldLabel);

            const choiceField = document.createElement('select');
            choiceField.name = `choice_${fieldNamePrefix}_${i+1}`;
            shortChoices.forEach(choice=> {
                const option = document.createElement('option');
                option.value = choice;
                option.textContent = choice;
                if(shortStrikeValue === "atm" && choice == 0) {
                    option.selected = true;
                }
                choiceField.append(option);
            });
            fieldContainer.appendChild(choiceField);

            const fieldInput = document.createElement('input');
            fieldInput.type = "text";
            fieldInput.name = `input_${fieldNamePrefix}_${i+1}`;
            fieldInput.placeholder = `Enter ${fieldNamePrefix} Value ${i+1}`;
            fieldContainer.appendChild(fieldInput);

            const optimizeCheckBox = document.createElement('input');
            optimizeCheckBox.type = "checkbox";
            optimizeCheckBox.name = `optimize_${fieldNamePrefix}_${i+1}`;
            optimizeCheckBox.disabled=true;
            fieldContainer.appendChild(optimizeCheckBox);

            const optimizeLabel = document.createElement('label');
            optimizeLabel.textContent = "Optimize";
            fieldContainer.appendChild(optimizeLabel);

            const maxLabel = document.createElement('label');
            maxLabel.textContent = "Max:";
            fieldContainer.appendChild(maxLabel);
            maxLabel.style.display = "none";

            const maxInput = document.createElement('input');
            maxInput.type = "text";
            maxInput.name = `max_${fieldNamePrefix}_${i+1}`;
            maxInput.placeholder = "Max Value";
            fieldContainer.appendChild(maxInput);
            maxInput.style.display = "none";

            const minLabel = document.createElement('label');
            minLabel.textContent = "Min:";
            fieldContainer.appendChild(minLabel);
            minLabel.style.display = "none";

            const minInput = document.createElement('input');
            minInput.type = "text";
            minInput.name = `min_${fieldNamePrefix}_${i+1}`;
            minInput.placeholder = "Min Value";
            fieldContainer.appendChild(minInput);
            minInput.style.display = "none";

            const stepLabel = document.createElement('label');
            stepLabel.textContent = "Step:";
            fieldContainer.appendChild(stepLabel);
            stepLabel.style.display = "none";

            const stepInput = document.createElement('input');
            stepInput.type = "text";
            stepInput.name = `step_${fieldNamePrefix}_${i+1}`;
            stepInput.placeholder = "Step Value";
            fieldContainer.appendChild(stepInput);
            stepInput.style.display = "none";

            // optimizeCheckBox.addEventListener("change", function() {
            //     if (this.checked) {
            //         maxInput.style.display = 'inline-block';
            //         minInput.style.display = 'inline-block';
            //         stepInput.style.display = 'inline-block';
            //         maxLabel.style.display = "inline-block";
            //         minLabel.style.display = "inline-block";
            //         stepLabel.style.display = "inline-block";

            //     } else {
            //         maxInput.style.display = 'none';
            //         minInput.style.display = 'none';
            //         stepInput.style.display = 'none';
            //         maxLabel.style.display = "none";
            //         minLabel.style.display = "none";
            //         stepLabel.style.display = "none";
            //     }
            // });
            dynamicFieldsShortContainer.appendChild(fieldContainer);
            } 
            else {
                const outerContainer = document.createElement('div');
                outerContainer.id = "fields";
                for(let j=0; j<greeksNames.length; j++) {
                    const innerContainer = document.createElement('div');
                    innerContainer.id = "field_container";
                    const inputFieldLabel = document.createElement('label');
                    inputFieldLabel.textContent = `${greeksNames[j].toUpperCase()}_${i+1}`;
                    innerContainer.appendChild(inputFieldLabel);

                    const inputChoiceField = document.createElement('select');
                    inputChoiceField.name = `choice_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    greeksChoices.forEach(choice=> {
                        const option = document.createElement('option');
                        option.value = choice;
                        option.textContent = choice;
                        inputChoiceField.append(option);
                    });
                    innerContainer.appendChild(inputChoiceField);

                    const fieldInput = document.createElement('input');
                    fieldInput.type = "number";
                    fieldInput.placeholder = "Enter Delta Value";
                    fieldInput.name = `input_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    innerContainer.appendChild(fieldInput);

                    const optimizeCheckBox = document.createElement('input');
                    optimizeCheckBox.type = "checkbox";
                    optimizeCheckBox.name = `optimize_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    optimizeCheckBox.disabled = true;
                    innerContainer.appendChild(optimizeCheckBox);

                    const optimizeLabel = document.createElement('label');
                    optimizeLabel.textContent = "Optimize ";
                    innerContainer.appendChild(optimizeLabel);

                    const maxLabel = document.createElement('label');
                    maxLabel.textContent = "Max:";
                    innerContainer.appendChild(maxLabel);
                    maxLabel.style.display = "none";

                    const maxInput = document.createElement('input');
                    maxInput.type = "text";
                    maxInput.name = `max_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    maxInput.placeholder = "Max Value";
                    innerContainer.appendChild(maxInput);
                    maxInput.style.display = "none";

                    const minLabel = document.createElement('label');
                    minLabel.textContent = "Min:";
                    innerContainer.appendChild(minLabel);
                    minLabel.style.display = "none";

                    const minInput = document.createElement('input');
                    minInput.type = "text";
                    minInput.name = `min_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    minInput.placeholder = "Min Value";
                    innerContainer.appendChild(minInput);
                    minInput.style.display = "none";

                    const stepLabel = document.createElement('label');
                    stepLabel.textContent = "Step:";
                    innerContainer.appendChild(stepLabel);
                    stepLabel.style.display = "none";

                    const stepInput = document.createElement('input');
                    stepInput.type = "text";
                    stepInput.name = `step_${greeksNames[j]}_${fieldNamePrefix}_${i+1}`;
                    stepInput.placeholder = "Step Value";
                    innerContainer.appendChild(stepInput);
                    stepInput.style.display = "none";

                    // optimizeCheckBox.addEventListener("change", function() {
                    //     if (this.checked) {
                    //         maxInput.style.display = 'inline-block';
                    //         minInput.style.display = 'inline-block';
                    //         stepInput.style.display = 'inline-block';
                    //         maxLabel.style.display = "inline-block";
                    //         minLabel.style.display = "inline-block";
                    //         stepLabel.style.display = "inline-block";
                    //     } else {
                    //         maxInput.style.display = 'none';
                    //         minInput.style.display = 'none';
                    //         stepInput.style.display = 'none';
                    //         maxLabel.style.display = "none";
                    //         minLabel.style.display = "none";
                    //         stepLabel.style.display = "none";
                    //     }
                    // });
                    outerContainer.appendChild(innerContainer);
                    dynamicFieldsShortContainer.appendChild(outerContainer);
                }
            }
        }
        
    }
});