const scriptName = "kakao";
const SERVER_URL = "http://146.56.166.180:8000/get_kakao_response"; // FastAPI 서버 URL
const SERVER_URL_OLD = "http://146.56.166.180:8000/get_kakao_response_old"; // FastAPI 서버 URL
/**
 * (string) room
 * (string) sender
 * (boolean) isGroupChat
 * (void) replier.reply(message)
 * (boolean) replier.reply(room, message, hideErrorToast = false) // 전송 성공시 true, 실패시 false 반환
 * (string) imageDB.getProfileBase64()
 * (string) packageName
 */
function response(room, msg, sender, isGroupChat, replier, imageDB, packageName) { 
    if (msg.includes("@딥챗봇")) {
        try {
            const requestData = {
                room: room,
                msg: msg,
                sender: sender,
                isGroupChat: isGroupChat
            };

            const json = org.jsoup.Jsoup.connect(SERVER_URL)
                .header("Content-Type", "application/json")
                .requestBody(JSON.stringify(requestData))
                .ignoreContentType(true)
                .post()
                .text();
            const data = JSON.parse(json);
            const reply = data.response || "응답을 가져올 수 없습니다.";
            if (reply !== "응답을 가져올 수 없습니다.") {
                replier.reply(reply);
            }
        } catch (parseError) {
            replier.reply("서버 응답을 처리하는 중 오류가 발생했습니다.");
        }
    }
    else if(sender == "장인우" || sender == "최준철" || sender == "조원준" || sender == "황인록 pippin.hobbit" ) {
        if (msg.includes("ㅎㅇ")) {
            let currentHour = new Date().getHours(); // 현재 시간을 가져옴
            let response;

            if (currentHour >= 5 && currentHour < 12) {
                let responses = ["Good Morning~!(음표)", "좋은 아침~!"];
                response = responses[Math.floor(Math.random() * responses.length)];
            } else if (currentHour >= 12 && currentHour < 18) {
                let responses = ["Good Afternoon~!", "Hello, Everyone!"];
                response = responses[Math.floor(Math.random() * responses.length)];
            } else {
                let responses = ["Good Evening~!(와인)", "좋은 저녁~!"];
                response = responses[Math.floor(Math.random() * responses.length)];
            }

            replier.reply(response);
        } else if (msg.includes("ㄱㅊ?")) {
            let responses1 = ["괜춘괜춘~", "그건 쫌 별루다..."];
            let response = responses1[Math.floor(Math.random() * responses1.length)];
            replier.reply(response);
        }
        else if (msg.includes("후회~")) {
            let responses1 = ["하고있어요~"];
            let response = responses1[Math.floor(Math.random() * responses1.length)];
            replier.reply(response);
        } 
        else if (msg.includes("ㅇㅈ?")) {
            let responses2 = ["ㅇㅈㅇㅈㄸㅇㅈ!", "ㄴㅇㅈ","(정색)","(최고)"];
            let response = responses2[Math.floor(Math.random() * responses2.length)];
            replier.reply(response);
        } 
        else if (msg.includes("!주사위")) {
            let diceRoll = Math.floor(Math.random() * 6) + 1;
            let response = `주사위 결과: [`+diceRoll+`]`;
            replier.reply(response);
        } 
        else if (msg.includes("ㄱㅇㅇ")) {
            let response = '커여웡!!!!!';
            replier.reply(response);
        }
        else if (msg.includes("은호") || msg.includes("일라이") || msg.includes("지운") || msg.includes("지율")) {
            let response = '넘나 커여운것!!!!!(신나)';
            replier.reply(response);
        }
        else if (msg.includes(" 혁")) {
            let responses3 = ["대 상 혁 (잘난척)", "페 이 커 (잘난척)"];
            let response = responses3[Math.floor(Math.random() * responses3.length)];
            replier.reply(response);
        } 
        else if (msg.includes("ㄷㄷ")) {
            let responses4 = ["(공포)", "(좌절)"];
            let response = responses4[Math.floor(Math.random() * responses4.length)];
            replier.reply(response);
        } 
        else if (msg.includes("상혁")) {
            let responses5 = ["대 상 혁 (잘난척)", "페 이 커 (잘난척)"];
            let response = responses5[Math.floor(Math.random() * responses5.length)];
            replier.reply(response);
        } 
        else if (msg.includes("vs") || msg.includes("VS")) {
            let parts = msg.split("vs").map(part => part.trim());
            if (parts.length === 2) {
                let response = parts[Math.floor(Math.random() * parts.length)];
                replier.reply(response);
            } else {
                replier.reply("올바른 형식으로 입력해 주세요! (예: A vs B)");
            }
        } 
        else if (msg.includes("ㅋㅋㅋㅋㅋㅋㅋㅋㅋ")) {
            let responses6 = [
                "(크크)",
                "(좋아)",
                "ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
                ""
            ];
            let response = responses6[Math.floor(Math.random() * responses6.length)];
            replier.reply(response);
        } 
    }
}

//아래 4개의 메소드는 액티비티 화면을 수정할때 사용됩니다.
function onCreate(savedInstanceState, activity) {
  var textView = new android.widget.TextView(activity);
  textView.setText("Hello, World!");
  textView.setTextColor(android.graphics.Color.DKGRAY);
  activity.setContentView(textView);
}

function onStart(activity) {}

function onResume(activity) {}

function onPause(activity) {}

function onStop(activity) {}