document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const formCard = document.querySelector('.form-card');
    const resultCard = document.getElementById('result-card');
    const resultCircle = document.getElementById('result-circle');
    const predictionText = document.getElementById('prediction-text');
    const confidenceText = document.getElementById('confidence-text');
    const progressFill = document.getElementById('progress-fill');
    const resetBtn = document.getElementById('reset-btn');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.getElementById('spinner');

    // API URL - change this if deploying to a remote server
    const API_URL = 'http://localhost:8000/predict';

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;

        // Gather form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Convert numeric fields
        data.ApplicantIncome = parseFloat(data.ApplicantIncome);
        data.CoapplicantIncome = parseFloat(data.CoapplicantIncome);
        data.LoanAmount = parseFloat(data.LoanAmount);
        data.Loan_Amount_Term = parseFloat(data.Loan_Amount_Term);
        data.Credit_History = parseFloat(data.Credit_History);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Prediction failed. Please ensure the backend is running.');
            }

            const result = await response.json();

            // Hide form, show result
            formCard.classList.add('hidden');
            resultCard.classList.remove('hidden');

            // Reset classes
            resultCircle.className = 'result-circle';

            // Apply result styles
            setTimeout(() => {
                if (result.prediction === 'Approved') {
                    resultCircle.classList.add('approved');
                    predictionText.textContent = 'Approved';
                } else {
                    resultCircle.classList.add('rejected');
                    predictionText.textContent = 'Rejected';
                }

                // Animate confidence bar
                const confidence = result.confidence;
                confidenceText.textContent = confidence;
                progressFill.style.width = `${confidence}%`;
            }, 100);

        } catch (error) {
            alert(error.message);
        } finally {
            // Reset loading state
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        resultCard.classList.add('hidden');
        formCard.classList.remove('hidden');
        progressFill.style.width = '0%';
        form.reset();
    });
});
