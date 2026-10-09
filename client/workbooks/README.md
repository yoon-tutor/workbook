# 정본

검증된 정본을 `<이름>/content.json`에 둡니다. `workbook_authoring_expand`의 결과를 `--into workbooks/<이름>`으로 저장하며, 클라이언트는 이미 있는 `content.json`을 덮어쓰지 않습니다.

검토가 끝난 정본은 packet으로 다시 만들어 덮어쓰지 않습니다. 내용을 고칠 때는 해당 문장·활동만 고치고 `contentVersion`과 업데이트 정의를 함께 올립니다.
