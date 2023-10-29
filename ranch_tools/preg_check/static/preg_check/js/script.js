document.addEventListener('DOMContentLoaded', function() {
	// Function definitions

    // Function for handling Edit Cow Modal
    function handleEditCowModal() {
        var modal = document.getElementById("editCowModal");
        var editButton = document.getElementById("edit-cow-btn");

        if (editButton) {
            // Show modal
            document.getElementById("edit-cow-btn").onclick = function() {
                modal.style.display = "block";
            }
        }

        // Hide modal
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    }

    // Event listeners for Edit Cow Modal
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	function updateStats() {
        // Make an AJAX request to fetch the summary stats
        const statsContent = document.getElementById('stats-content');
        const breedingSeason = document.getElementById('breeding-season-input').value;

        // Check if breedingSeason is numeric and has a length of 4
        if (breedingSeason.length === 4 && !isNaN(breedingSeason)) {
            fetch(pregcheckSummaryStatsUrl + '?stats_breeding_season=' + breedingSeason)
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
        } else {
            statsContent.innerHTML = 'Please provide a valid 4-digit breeding season.';
        }
    }

    function populateEmptyBreedingSeasonInput() {
        var breedingSeasonInput = document.getElementById('breeding-season-input');
        // Check if the input is empty
        if (!breedingSeasonInput.value) {
            // Set the input value to the latest breeding season provided by Django's context
            breedingSeasonInput.value = latestBreedingSeason;
            document.getElementById('breeding_season').value = latestBreedingSeason;
            updateStats();
        }
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
                updateStats();
				// Display success message
				messageContainer.textContent = 'PregCheck created successfully';
				messageContainer.classList.add('success');
				modal.style.display = 'block';
                setTimeout(function() {
                    modal.style.display = 'none';
                    location.href = pregchecksUrl;
                }, 2000);
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

	function closePregCheckEditModal() {
		var modal = document.getElementById('edit-modal');
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

	// Function to populate the edit modal with data
    function populateEditModal(pregcheckData) {
        // Populate form fields in the edit modal with data from pregcheckData
        document.getElementById('edit-pregcheck-id').value = pregcheckData.id;
        document.getElementById('edit-is_pregnant').value = pregcheckData.is_pregnant.toString();
        document.getElementById('edit-comments').value = pregcheckData.comments;
        document.getElementById('edit-recheck').value = pregcheckData.recheck;
        
        // Show the edit modal
        const editModal = document.getElementById('edit-modal');
        editModal.style.display = 'block';
    }

	// Event Listeners
    document.querySelector('#edit-modal .close').addEventListener('click', closePregCheckEditModal);
    document.querySelector('#no-animal-modal .close').addEventListener('click', closeNoAnimalModal);
    document.getElementById('cancel-create-btn').addEventListener('click', closeNoAnimalModal);
	document.getElementById('pregcheck-form').addEventListener('submit', handleFormSubmit);
	document.querySelector('.close').addEventListener('click', handleModalCloseBtnClick);

    // Listen to Breeding Season input and update stats
    document.querySelector('#breeding-season-input').addEventListener('input', function() {
        var breedingSeason = this.value;
        if(breedingSeason && breedingSeason.length === 4) {
            updateStats();
            document.getElementById('breeding_season').value = breedingSeason;
        }
    });

	// Event Listener for close edit modal
    const closeModalBtn = document.querySelector('#editCowModal .close-button');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            const modal = document.getElementById('editCowModal');
            modal.style.display = 'none';
        });
    }
    // Event listener for "edit" buttons
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', () => {
            const pregcheckId = button.getAttribute('data-pregcheck-id');
            
            // Make an AJAX request to fetch data for the selected pregcheck
            fetch(`/pregchecks/${pregcheckId}/`)
                .then(response => response.json())
                .then(data => {
                    populateEditModal(data);
                })
                .catch(error => {
                    console.error('Error fetching pregcheck data:', error);
                });
        });
    });

	// Event listener for "Save" button in the edit modal
    document.getElementById('edit-pregcheck-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent normal form submission
        
        const formData = new FormData(this);
        const pregcheckId = document.getElementById('edit-pregcheck-id').value;
        
        fetch(`/pregchecks/${pregcheckId}/edit/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Handle success (e.g., close modal, update UI)
                closePregCheckEditModal();
                location.reload();
            } else if (data.errors) {
                // Handle form errors (e.g., display error messages)
                console.error('Form errors:', data.errors);
            } else {
                // Handle other errors or unexpected responses
                console.error('Unexpected response:', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });


	window.addEventListener('click', handleWindowClick);


	// Initial Actions
	updateStats();
	handleCreateAnimal();
    handleEditCowModal();
    populateEmptyBreedingSeasonInput();
});

