async function sendMessage() {
	const messageObject = createMessageObject();
	const csrfToken = document.getElementById("csrfToken").value;
	let messageForm = new FormData();
	messageForm.append("messageField", messageField.value); // append = anhängen
	messageForm.append("csrfmiddlewaretoken", csrfToken);

	try {
		createTemporaryHtmlTemplateMessage(messageObject);
		await respondChat(messageForm);

		// let response = await fetch("/chat/", {
		// 	method: "POST",
		// 	body: messageForm,
		// });

		// let json = await response.json();
		// console.log("json is: ", json);
		removeTemporaryHtmlTemplateMessage();
		createHtmlTemplateMessage(messageObject);

		console.log("Send message succes!");
	} catch (e) {
		console.error("FAIL send message!", e);
	}
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
        <div id="messagePreview" class="htmlTemplateMessage">
            <span class="color-gray">[ ${messageObject.date} ]</span>
            
            <i class="color-gray">&nbsp;${messageObject.userName}:&nbsp;</i> <span class="color-gray">${messageObject.message}</span>
        </div>
        `);
}

async function respondChat(messageForm) {
	await fetch("/chat/", {
		method: "POST",
		body: messageForm,
	});
}

function removeTemporaryHtmlTemplateMessage() {
	return document.getElementById("messagePreview").remove();
}

function createHtmlTemplateMessage(messageObject) {
	return (messageContainer.innerHTML += `
		<div class="htmlTemplateMessage">
		    <span class="color-gray">[ ${messageObject.date} ]</span>
		    <i>&nbsp;${messageObject.userName}:&nbsp; </i> <span>${messageObject.message}</span>
		</div>
		`);
}
