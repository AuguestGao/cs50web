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
  
  // empty show div everytime change a mail
  document.querySelector('#show').innerHTML = '';
  
  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    emails.forEach(email => {
      //console.log(email.subject);cd
      const element = document.createElement('div');
      
      // set border and background accordingly
      element.setAttribute('class', 'div-border');
      
      if (email.read === true ) {
        element.setAttribute('id', 'read');
      } else {
        element.setAttribute('id', 'unread');
      }
      //console.log(email.id);
      element.innerHTML = `<p><strong>${email.sender}</strong> | ${email.subject} <span style='float:right'>${email.timestamp}</span><p>`;
      document.querySelector('#show').append(element);

      // go to email when click
      element.addEventListener('click', () => {
        //turn off unrelated divs
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        //empty corresponding div
        document.querySelector('#show').innerHTML = '';
        //console.log(email.id + "is clicked");
        view_email(email.id);
      });

    });
  });
  
}

function view_email(id) {
  
  fetch('/emails/'+id)
  .then(response => response.json())
  .then(email =>{

    const element = document.createElement('div');
    element.innerHTML = `<p><strong>From:</strong> ${email.sender}</p> <p><strong>To:</strong> ${email.recipients}</p> <p><strong>Subject:</strong> ${email.subject}</p> <p><strong>Timestamp:</strong> ${email.timestamp}</p>`;
    
    // reply button
    const reply = document.createElement('submit');
    reply.setAttribute('class', 'btn btn-outline-primary');
    reply.textContent='Reply';

    // automatically change to read
    toggle_status(id, 'read', true);

    reply.onclick = () => {
      console.log('replying'+email.id);
    };

    //add div, reply button nd line break
    document.querySelector('#show').append(element, reply, document.createElement('hr'));
  });
}

function toggle_status(id, name, status) {
  //console.log('in toggling');
  var change;
  const url = '/emails/' + id;

  if (name === "archive") {
    change = {archived: status};
    console.log('change archive');
  } else {
    change = {read: status};
    console.log('change read');
  }

  fetch(url, {
    method: 'PUT',
    body: JSON.stringify(change)
  })
}