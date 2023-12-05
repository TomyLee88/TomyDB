const deleteBtn = document.getElementById('deleteBtn');
        
deleteBtn.addEventListener('click', function(){
    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    confirmationModal.show();
    
});