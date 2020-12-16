document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
  document.querySelector('#compose-form').onsubmit = (event) => {
    
    // prevent auto-reloading (not show console.log and reload to index page)
    event.preventDefault();

    //send email
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      // print result
      console.log(result);
    })
    .catch(error => {
      console.log('Error', error);
    });

    load_mailbox('sent');
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // empty summary div everytime change a mail
  document.querySelector('#summary').innerHTML = '';

  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {
      //console.log(email.subject);
      const element = document.createElement('div');
      element.setAttribute('id', 'border');
      element.innerHTML = `<p><strong>${email.sender}</strong> | ${email.subject} <span style='float:right'>${email.timestamp}</span><p>`;
      document.querySelector('#summary').append(element);
      element.addEventListener('click', () => {
        console.log(email.id + "is clicked");
      });
    });
  });
  
}

