document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(args={}) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#show').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  // check if args has content
  if (Object.keys(args).length == 0) {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    document.querySelector('#compose-recipients').value = args.recipient;
    document.querySelector('#compose-subject').value = args.subject;
    document.querySelector('#compose-body').value = args.body;
  }
  
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
  document.querySelector('#show').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // empty show div everytime change a mail
  document.querySelector('#show').innerHTML = '';
  
  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
    //console.log(emails);
    emails.forEach(email => {
      //console.log(email.subject);cd
      const element = document.createElement('div');
      
      // set border and background accordingly     
      if (email.read === true ) {
        element.setAttribute('class', 'read div-border');
      } else {
        element.setAttribute('class', 'unread div-border');
      }

      element.setAttribute('id', 'id'+email.id);
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
        view_email(email.id, mailbox);
      });

    });
  });
}

function view_email(id, mailbox) {
  
  fetch('/emails/'+id)
  .then(response => response.json())
  .then(email =>{
    
    // automatically change to read
    toggle_status(id, 'read', true);

    const element = document.createElement('div');
    element.innerHTML = `<p><strong>From:</strong> ${email.sender}</p> <p><strong>To:</strong> ${email.recipients}</p> <p><strong>Subject:</strong> ${email.subject}</p> <p><strong>Timestamp:</strong> ${email.timestamp}</p>`;
    
    // reply button
    const bt_reply = document.createElement('submit');
    bt_reply.setAttribute('class', 'btn btn-outline-primary');
    bt_reply.textContent='Reply';
    
    //archive button
    const bt_arc = document.createElement('submit');
    bt_arc.setAttribute('class', 'btn btn-outline-warning');
    if (email.archived === true) {
      bt_arc.textContent = "Unarchive";
      bt_arc.value = false;
      bt_arc.name = 'archive';
    } else {
      bt_arc.textContent = "Archive";
      bt_arc.value = true;
      bt_arc.name = 'archive';
    }
    
    const bt_unread = document.createElement('submit');
    bt_unread.setAttribute('class','btn btn-outline-success');
    bt_unread.textContent = "Mark as Unread";
    bt_unread.value = false;
    bt_unread.name = 'read';

    bt_reply.onclick = () => {
      console.log("sent from: "+email.sender);
      var args ={
        recipient: email.sender,
        subject: "Re: " + email.subject,
        body: "\n\n" + "On " + email.timestamp + "\n" + email.sender + " wrote:\n" + email.body
      };
      compose_email(args);
    };

    //when bt_arc (archive button" is clicked), set archive status thru toggle_status function and load archive mailbox
    bt_arc.onclick = () => {
      toggle_status(id, bt_arc.name, bt_arc.value);
      load_mailbox('inbox');
    };

    bt_unread.onclick = () => {
      toggle_status(id, bt_unread.name, bt_unread.value);
      load_mailbox('inbox');
    };

    const email_body = document.createElement('pre');
    email_body.innerHTML = `${email.body}`;
  
    //add div, reply button nd line break
    //if it's from 'sent' page, ignore bt_arc
    if (mailbox != 'sent') {
      if (mailbox != 'archive') {
        document.querySelector('#show').append(element, bt_reply, bt_arc, bt_unread, document.createElement('hr'), email_body);
      } else {
        document.querySelector('#show').append(element, bt_reply, bt_arc, document.createElement('hr'), email_body);
      }
    } else {
      document.querySelector('#show').append(element, bt_reply, document.createElement('hr'), email_body);
    }
  });
}

function toggle_status(id, name, status) {
  //console.log('in toggling');
  var change;
  const url = '/emails/' + id;

  if (name === "archive") {
    change = {archived: status};
    //console.log('change archive');
  } else {
    change = {read: status};
    //console.log('change read to' +status);
  }

  fetch(url, {
    method: 'PUT',
    body: JSON.stringify(change)
  });
}