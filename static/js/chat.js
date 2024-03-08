async function sendMessage() {
	const messageObject = createMessageObject();
	const csrfToken = document.getElementById("csrfToken").value;
	let messageForm = new FormData();
	messageForm.append("messageField", messageField.value); // append = anhängen
	messageForm.append("csrfmiddlewaretoken", csrfToken);

	try {
		createNewMessage(messageObject, messageForm);
		clearInput(messageField);
		console.log("Send message succes!");
	} catch (e) {
		console.error("FAIL send message!", e);
	}
}

async function createNewMessage(messageObject, messageForm) {
	createTemporaryHtmlTemplateMessage(messageObject);
	let responseChat = await respondChat(messageForm);
	let jsonChat = await responseChat.json();
	removeTemporaryHtmlTemplateMessage();
	createHtmlTemplateMessage(jsonChat);
}

function createMessageObject() {
	return {
		date: createNewDate(),
		userName: document.getElementById("userName").value,
		message: messageField.value,
	};
}

function createNewDate() {
	let currentDate = new Date();

	var formattedDate =
		shortcuttedMonth[currentDate.getMonth()] +
		" " +
		currentDate.getDate() +
		", " +
		currentDate.getFullYear();

	return formattedDate;
}

function createTemporaryHtmlTemplateMessage(messageObject) {
	return (messageContainer.innerHTML += `
		<div class="message__right">
    	    <div id="messagePreview" class="message--user message__bubble--user htmlTemplateMessage">
				<div>
    	        	<span class="color-gray">[ ${messageObject.date} ]</span>
    	        	<i class="color-gray">&nbsp;${messageObject.userName}:&nbsp;</i> 
				</div>	
				<span class="color-gray">${messageObject.message}</span>
    	    </div>
		</div>
        `);
}

async function respondChat(messageForm) {
	return await fetch("/chat/", {
		method: "POST",
		body: messageForm,
	});
}

function removeTemporaryHtmlTemplateMessage() {
	return document.getElementById("messagePreview").remove();
}

function createHtmlTemplateMessage(messageObject) {
	return (messageContainer.innerHTML += `
		<div class="message__right">
			<div class="message--user message__bubble--user htmlTemplateMessage">
				<div>
			    	<span class="color-gray">[ ${messageObject.fields.created_at} ]</span>
			    	<i>&nbsp;${messageObject.fields.author_name}:&nbsp; </i> 
				</div>	
				<span>${messageObject.fields.text}</span>
			</div>
		</div>
		`);
}

function clearInput(inputField) {
	inputField.value = "";
}
