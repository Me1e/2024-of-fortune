// "tell-story" 버튼에 클릭 이벤트 리스너를 추가합니다.
document.getElementById('tell-story').addEventListener('click', async () => {
  // 입력 필드에서 사용자가 입력한 스토리 토픽을 가져옵니다.
  const name = document.getElementById('name').value.trim();
  if (!name) return; // 스토리가 비어있으면 아무 것도 하지 않습니다.

  // 스토리 출력 및 진행 상태 표시 요소를 가져옵니다.
  const storyOutput = document.getElementById('story-output');
  const storyProgress = document.getElementById('story-progress');
  storyOutput.innerText = ''; // 스토리 출력 초기화
  storyProgress.innerText = '...'; // 진행 상태 표시

  // 서버에 스토리 생성 요청을 보냅니다.
  const response = await fetch('/api/story', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
  if (!response.ok) return; // 요청 실패 시 중단

  // 스트리밍 방식으로 응답을 받아 처리합니다.
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  // 서버로부터 데이터가 모두 전송될 때까지 반복합니다.
  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      // 데이터 전송이 완료되면 진행 상태를 비웁니다.
      storyProgress.innerText = '';
      break;
    }
    // 받은 데이터를 디코딩하여 스토리 출력에 추가합니다.
    storyOutput.innerText += decoder.decode(value);
  }
});
