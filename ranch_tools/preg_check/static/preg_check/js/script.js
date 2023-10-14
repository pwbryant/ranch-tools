document.addEventListener('DOMContentLoaded', function() {
	// Function definitions
	function updateStats() {
		// Make an AJAX request to fetch the summary stats
		const statsContent = document.getElementById('stats-content');
		fetch(pregcheckSummaryStatsUrl)
			.then(response => response.json())
			.then(data => {
				// Update the stats content with the fetched data
				statsContent.innerHTML = `
					<h2>Summary Stats</h2>
					<p>Total Pregnant: ${data.total_pregnant}</p>
					<p>Total Open: ${data.total_open}</p>
					<p>Total Count: ${data.total_count}</p>
					<p>Pregnancy Rate: ${data.pregnancy_rate.toFixed(2)}%</p>
				`;
			})
			.catch(error => {
				console.error('Error fetching summary stats:', error);
				statsContent.innerHTML = 'Error fetching summary stats.';
			});
	}

	function handleFormSubmit(event) {
		event.preventDefault(); // Prevent normal form submission
		var form = document.getElementById('pregcheck-form');
		var messageContainer = document.getElementById('message-container');
		var modal = document.getElementById('message-modal');
		var formData = new FormData(form);

		var xhr = new XMLHttpRequest();
		xhr.open(form.method, form.action, true);
		xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
		xhr.onload = function() {
			if (xhr.status === 200) {
				// Display success message
				messageContainer.textContent = 'PregCheck created successfully';
				messageContainer.classList.add('success');
				modal.style.display = 'block';

				// Reset the form inputs
				form.reset();
				document.getElementById('id_search_animal_id').value = '';
				document.getElementById('id_search_birth_year').value = '';
				// Remove animal_id input and label
				var animalIdInput = document.getElementById('id_pregcheck_animal_id');
				var animalIdLabel = document.querySelector('label[for="id_pregcheck_animal_id"]');
				if (animalIdInput && animalIdLabel) {
					animalIdInput.remove();
					animalIdLabel.remove();
				}

				// Clear result container
				var resultContainer = document.querySelector('.result-container');
				if (resultContainer) {
					resultContainer.innerHTML = '';
				}

				// Update summary stats
				updateStats();

				// Remove query parameters from URL
				if (window.history && window.history.replaceState) {
					var newUrl = window.location.href.split('?')[0];
					window.history.replaceState({ path: newUrl }, '', newUrl);
				}
			} else {
				// Display error message
				messageContainer.textContent = 'Something went wrong';
				messageContainer.classList.add('error');
				modal.style.display = 'block';
			}
		};
		xhr.onerror = function() {
			// Display error message
			messageContainer.textContent = 'Something went wrong';
			messageContainer.classList.add('error');
			modal.style.display = 'block';
		};
		xhr.send(formData);
	}

	function handleContinueBtnClick() {
		var modal = document.getElementById('message-modal');
		modal.style.display = 'none';
	}

	function closeModal() {
		var modal = document.getElementById('message-modal');
		modal.style.display = 'none';
	}

	function handleModalCloseBtnClick() {
		closeModal();
	}

	function handleWindowClick(event) {
		var modal = document.getElementById('message-modal');
		if (event.target === modal) {
			closeModal();
		}
	}
	
	function handleCreateAnimal() {
		const noAnimalModal = document.getElementById('no-animal-modal');
		
		function openNoAnimalModal(animalId) {
			noAnimalModal.style.display = 'block';
			document.getElementById('new_animal_id').value = animalId;
		}

		function closeNoAnimalModal() {
			noAnimalModal.style.display = 'none';
		}

		if (animalExists === "False") {
			openNoAnimalModal(document.getElementById('id_search_animal_id').value);
		} else {
			closeNoAnimalModal();
		}

		return { openNoAnimalModal, closeNoAnimalModal };
	}

    const { closeNoAnimalModal } = handleCreateAnimal();

	// Event Listeners
    document.querySelector('#no-animal-modal .close').addEventListener('click', closeNoAnimalModal);
    document.getElementById('cancel-create-btn').addEventListener('click', closeNoAnimalModal);
	document.getElementById('pregcheck-form').addEventListener('submit', handleFormSubmit);
	document.getElementById('continue-btn').addEventListener('click', handleContinueBtnClick);
	document.querySelector('.close').addEventListener('click', handleModalCloseBtnClick);
	window.addEventListener('click', handleWindowClick);


	// Initial Actions
	updateStats();
	handleCreateAnimal();
});

