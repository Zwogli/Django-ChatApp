// {{ request.user.first_name }}
async function sendMessage(user) {
	let form = new FormData();
	let djangoToken = "{{ csrf_token }}";
	form.append("messagefield", messagefield.value); // append = anhängen
	form.append("csrfmiddlewaretoken", djangoToken);
	try {
		messageContainer.innerHTML += `
        <div id="messagePreview">
            <span class="color-gray">[Datum]</span>
            
            <i class="color-gray">${user}:</i> <div class="color-gray">${messagefield.value}</div>
        </div>
        `;
		// debugger;
		// await fetch("/chat/", {
		// 	method: "POST",
		// 	body: form,
		// });

		// document.getElementById("messagePreview").remove();
		// messageContainer.innerHTML += `
		// <div>
		//     <span class="color-gray">[Datum]</span>
		//     <i>{{ request.user.first_name }}:</i> <div>${messagefield.value}</div>
		// </div>
		// `;
		console.log("Send message succes!");
	} catch (e) {
		console.error("FAIL send message!", e);
	}
}
