(function() {

const discussionId = window.discussion_id;
const userId = window.user_pk;

const buttonUploadFile = document.querySelector('.discussion__save-file');
const buttonSendMessage = document.querySelector('.discussion__message-send');
const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${discussionId}/`);
buttonUploadFile.addEventListener('click', async function (event){
    await uploadFile(event, addFile);

});



socket.addEventListener('open', function() {
    buttonSendMessage.addEventListener('click', function() {
        const messageBody = addMessage();
        const { message, isMessageAdd, sending_user } = messageBody;
        if(isMessageAdd) {
            socket.send(JSON.stringify({ text_message: message, sending_user }))
        }
    });
})

socket.addEventListener('message', function(event) {
    const parseData = JSON.parse(event.data);
    addMessageFromServer(parseData);
})

}())

function addFile (dataFile) {
    const container = document.querySelector('.discussion__files .discussion__container_hiden');
    const {download_link, fileName} = dataFile
    const htmlStructure = `
                                <a href="${download_link}" target="_blank">
                                    <svg width="15" height="18" viewBox="0 0 15 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <mask id="path-1-inside-1_195_13" fill="white">
                                        <path d="M5.83337 0H12C13.6569 0 15 1.34315 15 3V15C15 16.6569 13.6569 18 12 18H5.83337V0Z"></path>
                                        </mask>
                                        <path d="M5.83337 -1H12C14.2092 -1 16 0.790861 16 3H14C14 1.89543 13.1046 1 12 1H5.83337V-1ZM16 15C16 17.2091 14.2092 19 12 19H5.83337V17H12C13.1046 17 14 16.1046 14 15H16ZM5.83337 18V0V18ZM12 -1C14.2092 -1 16 0.790861 16 3V15C16 17.2091 14.2092 19 12 19V17C13.1046 17 14 16.1046 14 15V3C14 1.89543 13.1046 1 12 1V-1Z" fill="#4282C4" mask="url(#path-1-inside-1_195_13)"></path>
                                        <path d="M0.521397 5.76087C0.772159 2.84412 3.19629 0.548375 6.16667 0.500755V5.76087H0.521397Z" fill="#4282C4" stroke="#4282C4"></path>
                                        <mask id="path-4-inside-2_195_13" fill="white">
                                        <path d="M0 6.26086H5.83333V18H2C0.895432 18 0 17.1046 0 16V6.26086Z"></path>
                                        </mask>
                                        <path d="M0 6.26086H5.83333H0ZM5.83333 19H2C0.343146 19 -1 17.6568 -1 16H1C1 16.5523 1.44772 17 2 17H5.83333V19ZM2 19C0.343146 19 -1 17.6568 -1 16V6.26086H1V16C1 16.5523 1.44772 17 2 17V19ZM5.83333 6.26086V18V6.26086Z" fill="#4282C4" mask="url(#path-4-inside-2_195_13)"></path>
                                        </svg>
                                    <p>
                                        ${fileName}
                                    </p>
                                </a>`

    const createItem = document.createElement('div');
    createItem.className = 'discussion__item';
    createItem.innerHTML = htmlStructure
    container.append(createItem)
}

async function uploadFile(event, callback) {
    const reader = new FileReader();
    const file = document.querySelector('.discussion__upload input').files[0];
    let download_link = ''
    let fileName = ''

    if(file) {
        reader.onload = async () => {
            const bufferReader = reader.result;
            fileName = file.name;
            discussionId = window.discussion_id;
            const url = '/attached_file/api/metaINF_file/';
            const XToken = getCookie('csrftoken');
            const dataSend = {
                discussion_id: discussionId,
                file_name: fileName,
            }
            const options = {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': XToken
                },
                body: JSON.stringify(dataSend),
            };
            const data = await fetch(url, options);
            const uploadURL = data.headers.get('Upload_url');

            await fetch(uploadURL, {
                method: 'PUT',
                body: bufferReader
            })
            download_link = data.headers.get('download_link');
            callback({download_link, fileName})
        }
        await reader.readAsArrayBuffer(file);

    }
}

function addMessageFromServer(data) {
    const { message, user, user_id, date_time } = data;
    const currentUserId = window.user_pk;

    if(currentUserId === user_id) return;

    const date = new Date(date_time);
    const containerAddMessage = document.querySelector('.discussion__message-wrapper');
    createStructureMessage = messageStructure({
        message,
        name: user,
        date: date.toLocaleDateString(),
        className: 'come',
    })
    const createItem = document.createElement('div');
    createItem.className = "discussion__message-item-come";
    createItem.innerHTML = createStructureMessage;
    containerAddMessage.append(createItem);

}

function messageStructure(dataMessage) {
    const { message, date, name, className } = dataMessage;
    return `<div class="discussion__message-item discussion__message-item_${className}">
        <p class="discussion__message-text">${message}</p>
        <div class="discussion__message-container">
            <span class="discussion__message-name">${name}</span>
            <span class="discussion__message-date">${date}</span>
        </div>
    </div>`
}

function addMessage() {
    const textMessage = document.querySelector('.discussion__message-input input');
    const valueText = textMessage.value;
    const containerAddMessage = document.querySelector('.discussion__message-wrapper');
    if(valueText) {
        textMessage.value = '';
        const now = Date.now();
        const nowDate = new Date(now);
        let dateString = nowDate.toLocaleDateString();
        const sending_user = window.username;

        const createStructureMessage = messageStructure({
            message: valueText,
            date: dateString,
            name: sending_user,
            className: 'send',
        })
        const createItem = document.createElement('div');
        createItem.className = "discussion__message-item-send";
        createItem.innerHTML = createStructureMessage;
        containerAddMessage.append(createItem);

        return {
            message: valueText,
            isMessageAdd: true,
            sending_user,
        }
    }
    return {
        isMessageAdd: false,
    }
}
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}