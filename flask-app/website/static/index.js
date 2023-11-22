function delete_note(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId })
    }).then((_res) => {
        window.location.href = "/"; //reloads the window after the delete
    });
}

function delete_translation(transId){
    fetch('/delete-translation', {
        method: 'POST',
        body: JSON.stringify({transId: transId })
    }).then((_res) => {
        window.location.href = "/translation"; //reloads the window after the delete
    });
}