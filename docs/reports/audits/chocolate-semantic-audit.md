# Chocolate canonical workbook 의미 품질 감사

- 감사 대상: `workbooks/chocolate/content.json`
- 기준: `docs/semantic-rubric.md` 1.0.0, `config/workbook-spec.json` 1.0.0
- 감사 범위: 원문 보존, 번역, 직독직해 1:1 대응, 서술어 표시, 어휘 쌍, 2·3·5·6·8·10단계 문장별 정답, 7·9단계 지문 활동
- 수정 여부: 최초 감사에서는 정본을 수정하지 않았고, 감사 승인 후 정본 교정 완료

> **최신 판정:** 정본 교정과 재검증을 완료했다. 이 문서 마지막의 `수정 후 재검증`이 현재 상태이며, 아래 최초 판정은 수정 전 기록으로 보존한다.

## 최초 판정 요약 (수정 전)

최초 감사 시점의 **의미 검수는 릴리스 불가**였다. 기계 구조 검증은 0건으로 통과했지만, 직독직해 영어 어순, 서술어 타깃, 단일 정답이 되지 않는 선택지에 확정 오류가 있었다.

| 구분 | 결과 |
|---|---:|
| canonical validator 구조 오류 | 0 |
| 원문→`display` 차이 | 0/24 |
| `meaningSegments[].en` 원문 복원 오류 | 0/24 |
| 8단계 chunk 원문 복원/순열 오류 | 0/24 |
| 어휘 영·한 쌍/색상 중복 오류 | 0 |
| 확정 의미 오류가 있는 문장 | 23/24 |
| 문장 단위 완전 통과 | 19번 1개 |

Validator는 CLI가 아직 없어 `workbook_engine.validator.validate_canonical()`을 직접 호출했다. 결과 0건은 스키마·타깃 해석·원문 복원 같은 **구조 통과**를 뜻하며, 아래 의미 판단을 보증하지는 않는다.

## 문장별 감사 결과

| 번호 | 판정 | 실제 오류 요약 |
|---:|---|---|
| 1 | P0 | `Delicious!`을 서술어로 표시, 직독직해 `맛있는!`, 5단계 비문 |
| 2 | P0 | `does ... come from`을 두 predicate로 잘못 분리하고 한국어 타깃 누락 |
| 3 | P1 | `ago`를 `전부터`로 확장하고 `starting + 시간`의 영어 어순 역전 |
| 4 | P0 | 주절 서술어 `were` 누락, 후치 부정사 `grow`를 서술어로 오표시 |
| 5 | P0 | `is thought`, `there is` 서술어 누락, `used + 목적어` 어순 역전 |
| 6 | P0 | `their` 의미 누락, `passed/made + 목적어` 어순 역전 |
| 7 | P0 | 6단계 `started to become / started becoming`이 둘 다 가능 |
| 8 | P0 | 6단계 `used cacao for trade / used cacao to trade`가 둘 다 문법적·문맥적으로 가능 |
| 9 | P1 | 직독직해 목적어 어순 역전, 2단계 재표현이 `when`을 단순 접속으로 변경 |
| 10 | P0 | 내포절 `were` 서술어 누락, `brought/knowing + 보충어` 어순 역전 |
| 11 | P1 | `arrived + 장소` 직독직해 어순 역전 |
| 12 | P0 | `earliest known`의 오역·추가, `had` 서술어 누락, 목적어 어순 역전 |
| 13 | P1 | `established + 목적어` 직독직해 어순 역전 |
| 14 | P1 | `took + 목적어·장소` 직독직해 어순 역전 |
| 15 | P1 | 완성 번역이 부자연스럽고 `was sweetened + with` 어순 역전 |
| 16 | P0 | 6단계 `was opened / opened`는 둘 다 가능, 장소 어순 역전 |
| 17 | P1 | `to drink + 목적어` 직독직해 어순 역전 |
| 18 | P1 | 완성 번역 `왕실에 의해서만 마셔질 수` 부자연스러움 |
| 19 | PASS | 확정 의미 오류 없음 |
| 20 | P0 | `boxes of chocolates` 오역, 직독직해 어순 역전, 6단계 복수/불가산 양쪽 가능 |
| 21 | P1 | `love the taste`를 `맛을 사랑한다`로 부자연스럽게 번역, 목적어 어순 역전 |
| 22 | P0 | 관계절 `will not go away` 서술어 누락, 5단계 cue가 정답 그대로 |
| 23 | P0 | 양태 포함 서술어 `can ... make`에서 `make`만 표시 |
| 24 | P0 | `Did ... know` 누락, 목적 부정사 `make` 오표시, `you` 누락·`라는` 추가 |

P0는 정답/학습 구조를 틀리게 보이게 하는 릴리스 차단 항목, P1은 번역·직독직해 품질 수정 항목이다.

## F-01. 직독직해 1:1 대응과 영어 어순 (P0/P1)

아래는 자연스러운 완성 번역이 아니라 1단계 `meaningSegments` 수정안이다. 서술어+목적어·보어·부사구를 한 단위에 뭉친 채 한국어 자연스러운 어순으로 뒤집은 패턴이 반복된다. 권장값의 `|`는 새 단위 경계다.

| JSON 경로 | 현재 `en ⇔ ko` | 권장 `en ⇔ ko` |
|---|---|---|
| `sentences[1].meaningSegments[1]` | `where does chocolate come from?` ⇔ `초콜릿은 어디에서 오는가?` | `where` ⇔ `어디에서` \| `does chocolate come from?` ⇔ `초콜릿은 유래하는가?` |
| `sentences[2].meaningSegments[2]` | `starting about 100 million years ago.` ⇔ `약 1억 년 전부터 시작하여.` | `starting` ⇔ `시작하여` \| `about 100 million years ago.` ⇔ `약 1억 년 전에.` |
| `sentences[3].meaningSegments[2]` | `to grow the cacao plant.` ⇔ `카카오 식물을 재배한.` | `to grow` ⇔ `재배한` \| `the cacao plant.` ⇔ `카카오 식물을.` |
| `sentences[4].meaningSegments[1]` | `that they used the cacao beans` ⇔ `그들이 카카오콩을 사용했다고` | `that they used` ⇔ `그들이 사용했다고` \| `the cacao beans` ⇔ `카카오콩을` |
| `sentences[5].meaningSegments[0]` | `The Olmecs passed their cacao knowledge` ⇔ `올멕족은 카카오 지식을 전했다` | `The Olmecs` ⇔ `올멕족은` \| `passed their cacao knowledge` ⇔ `전했다 자신들의 카카오 지식을` |
| `sentences[5].meaningSegments[2:4]` | `who made chocolate / into a spicy drink used in ceremonies.` ⇔ `그들은 초콜릿을 만들었다 / 의식에 사용되는 매운 음료로.` | `who` ⇔ `그들은` \| `made chocolate` ⇔ `만들었다 초콜릿을` \| `into a spicy drink` ⇔ `매운 음료로` \| `used in ceremonies.` ⇔ `의식에 사용되는.` |
| `sentences[6].meaningSegments[1]` | `to become very precious.` ⇔ `매우 귀중해지기.` | `to become` ⇔ `귀중해지기` \| `very precious.` ⇔ `매우 귀중하게.` |
| `sentences[7].meaningSegments[1]` | `the Aztecs used cacao for trade` ⇔ `아즈텍인들은 카카오를 무역에 사용했다` | `the Aztecs` ⇔ `아즈텍인들은` \| `used cacao for trade` ⇔ `사용했다 카카오를 무역에` |
| `sentences[8].meaningSegments[3]` | `when he and his crew captured a trade ship.` ⇔ `그와 선원들이 무역선을 나포했을 때.` | `when he and his crew captured` ⇔ `그와 그의 선원들이 나포했을 때` \| `a trade ship.` ⇔ `무역선을.` |
| `sentences[9].meaningSegments[2]` | `and brought them back to Europe,` ⇔ `그리고 그것들을 유럽으로 가져갔다` | `and brought` ⇔ `그리고 가져갔다` \| `them back to Europe,` ⇔ `그것들을 유럽으로,` |
| `sentences[9].meaningSegments[3]` | `not knowing the potential value of the unusual beans.` ⇔ `그 특이한 콩들의 잠재적 가치를 알지 못한 채.` | `not knowing` ⇔ `알지 못한 채` \| `the potential value of the unusual beans.` ⇔ `그 특이한 콩들의 잠재적 가치를.` |
| `sentences[10].meaningSegments[1]` | `arrived in Central America` ⇔ `중앙아메리카에 도착했다` | `arrived` ⇔ `도착했다` \| `in Central America` ⇔ `중앙아메리카에` |
| `sentences[11].meaningSegments[1]` | `he saw the Aztec Emperor drinking 'Xocalatl,'` ⇔ `그는 아즈텍 황제가 '소칼라틀'을 마시는 것을 보았다` | `he saw` ⇔ `그는 보았다` \| `the Aztec Emperor drinking 'Xocalatl,'` ⇔ `아즈텍 황제가 '소칼라틀'을 마시는 것을` |
| `sentences[11].meaningSegments[3]` | `and Cortés realised the great value` ⇔ `그리고 코르테스는 큰 가치를 깨달았다` | `and Cortés realised` ⇔ `그리고 코르테스는 깨달았다` \| `the great value` ⇔ `큰 가치를` |
| `sentences[12].meaningSegments[1]` | `Cortés established a cacao plantation` ⇔ `코르테스는 카카오 농장을 세웠다` | `Cortés established` ⇔ `코르테스는 세웠다` \| `a cacao plantation` ⇔ `카카오 농장을` |
| `sentences[13].meaningSegments[0]` | `He took the beans back to Spain` ⇔ `그는 그 콩들을 스페인으로 가져갔다` | `He took` ⇔ `그는 가져갔다` \| `the beans back to Spain` ⇔ `그 콩들을 스페인으로` |
| `sentences[14].meaningSegments[3]` | `and it was sweetened with sugar.` ⇔ `그리고 그것은 설탕으로 달게 되었다.` | `and it was sweetened` ⇔ `그리고 그 음료는 달게 되었다` \| `with sugar.` ⇔ `설탕으로.` |
| `sentences[15].meaningSegments[2]` | `was opened in London.` ⇔ `런던에 열렸다.` | `was opened` ⇔ `열렸다` \| `in London.` ⇔ `런던에.` |
| `sentences[16].meaningSegments[2]` | `to drink chocolate.` ⇔ `초콜릿을 마실.` | `to drink` ⇔ `마실` \| `chocolate.` ⇔ `초콜릿을.` |
| `sentences[19].meaningSegments[2]` | `were mass-producing boxes of chocolates.` ⇔ `초콜릿 상자들을 대량 생산하고 있었다.` | `were mass-producing` ⇔ `대량 생산하고 있었다` \| `boxes of chocolates.` ⇔ `상자에 든 초콜릿들을.` |
| `sentences[20].meaningSegments[2]` | `and people all over the world love the taste of chocolate.` ⇔ `그리고 전 세계 사람들이 초콜릿의 맛을 사랑한다.` | `and people all over the world love` ⇔ `그리고 전 세계 사람들은 좋아한다` \| `the taste of chocolate.` ⇔ `초콜릿의 맛을.` |
| `sentences[21].meaningSegments[1]` | `that will not go away any time soon.` ⇔ `곧 사라지지 않을.` | `that will not go away` ⇔ `사라지지 않을` \| `any time soon.` ⇔ `조만간.` |
| `sentences[23].meaningSegments[1:4]` | `To make a good chocolate / you only need four ingredients: / cocoa ... milk powder.` ⇔ `좋은 초콜릿을 만들기 위해 / 네 가지 재료만 필요하다 / ... 분유라는.` | `To make` ⇔ `만들기 위해` \| `a good chocolate` ⇔ `좋은 초콜릿을` \| `you` ⇔ `여러분에게는` \| `only need four ingredients:` ⇔ `필요하다 네 가지 재료만:` \| 재료 목록 ⇔ `카카오콩, 코코아 버터, 설탕, 분유.` |

이 수정으로 세그먼트 ID가 바뀌면 `annotations.predicates[].segmentId`, `annotations.vocabulary[].segmentId`와 타깃 occurrence를 같이 재생성해야 한다. 원문 문자열은 바꾸지 않는다.

## F-02. 서술어 strong 타깃 (P0)

| JSON 경로 | 현재값 | 권장값 |
|---|---|---|
| `sentences[0].annotations.predicates` | `Delicious ⇔ 맛있는` | 빈 배열. 형용사 단독 감탄 조각은 절의 서술어가 아님 |
| `sentences[1].annotations.predicates` | `does ⇔ 오는가`, 별도 `come from ⇔ (누락)` | predicate 1개로 통합: `en=[does, come from]`, `ko=[유래하는가]` |
| `sentences[3].annotations.predicates` | `grow ⇔ 재배한` | 현재 annotation 삭제, `s004-m02` 주절 `were ⇔ 사람들이었다` 추가 |
| `sentences[4].annotations.predicates` | `used` 1개만 존재 | `is thought ⇔ 여겨진다`, `used ⇔ 사용했다고`, `is ⇔ 없다` 세 절의 서술어 표시 |
| `sentences[9].annotations.predicates` | `presumed`, `brought` | 내포절의 `were ⇔ 종류였다고` 추가 |
| `sentences[11].annotations.predicates` | `saw`, `realised` | 관계절 `had ⇔ 가진` 추가 |
| `sentences[21].annotations.predicates` | 주절 `is`만 존재 | 관계절 `will not go away ⇔ 사라지지 않을` 추가 |
| `sentences[22].annotations.predicates` | `make ⇔ 만들 수 있다` | predicate 1개의 영어 target을 `can`, `make` 두 개로 두고 한국어 `만들 수 있다` 연결 |
| `sentences[23].annotations.predicates` | 목적 부정사 `make` 표시, `need` 표시 | `make` annotation 삭제; `Did`+`know` ⇔ `알고 있었나요` 추가; `need` 유지 |

`sentences[6]` (`started to become`)의 `become`을 핵심 보충어 부정사까지 strong 범위에 포함할지는 루브릭상 사람 판단이 필요하다. 현재 `started`만 표시한 것을 확정 오류 건수에는 넣지 않았다.

## F-03. 자연스러운 완성 번역 (P1)

| JSON 경로 | 현재값 | 권장값 |
|---|---|---|
| `sentences[11].translation` | `가장 이른 형태의 알려진 핫 초콜릿` | `최초의 핫초콜릿으로 알려진` (정확한 수식 범위는 전체 문장에서 재다듬기) |
| `sentences[14].translation` | `향신료들이 ... 더해졌고 그것은 설탕으로 달게 되었다` | `여기서는 계피와 다른 향신료가 그 쓴 음료에 첨가되었고, 설탕으로 단맛을 냈다.` |
| `sentences[17].translation` | `초콜릿이 오직 왕실에 의해서만 마셔질 수 있었다` | `사실 프랑스에서는 왕실 사람들만 초콜릿을 마실 수 있었다.` |
| `sentences[19].translation` | `초콜릿 상자들을 대량 생산` | `상자에 담은 초콜릿을 대량 생산` |
| `sentences[20].translation` | `초콜릿의 맛을 사랑한다` | `초콜릿 맛을 좋아한다` |

`sentences[11].meaningSegments[2].ko`의 `가장 이른 형태의 알려진`은 영어에 없는 `형태`를 추가하므로 `알려진 최초의 핫초콜릿인` 등으로 같이 고쳐야 한다.

## F-04. 6단계 단일 정답 실패 (P0)

| JSON 경로 | 현재 options | 문제 | 권장 options 예 |
|---|---|---|---|
| `sentences[6].exercises.choice.targets[0].options` | `to become / becoming` | `start to V`, `start V-ing` 모두 가능 | target을 `started` 등으로 바꾸고 `started / starting`처럼 문항 전면 재설계 |
| `sentences[7].exercises.choice.targets[0].options` | `for / to` | `used cacao to trade`도 문법적이고 문맥상 가능 | target을 `used`로 바꾸고 `used / using`처럼 한 쪽만 서술어가 되는 문항으로 재설계 |
| `sentences[15].exercises.choice.targets[0].options` | `was opened / opened` | `the first chocolate house opened in London`도 자동사 용법으로 완전한 문장 | `was opened / were opened` |
| `sentences[19].exercises.choice.targets[1].options` | `chocolates / chocolate` | `boxes of chocolates`(개별 초콜릿), `boxes of chocolate`(물질명사) 모두 가능 | `boxes / box` 등 수 표지가 명확한 문항으로 교체 |

권장 오답은 형식 예시다. 새 오답이 문법·의미상 하나만 틀리는지 사람이 다시 확인해야 한다.

## F-05. 5단계 동사형 문항 (P0/P1)

| JSON 경로 | 현재값 | 문제 | 권장값 |
|---|---|---|---|
| `sentences[0].exercises.verb.baseText` | `Chocolate bars.. Chocolate ice cream.. Chocolate milk.. are delicious!` | 마침표로 끝난 세 조각 뒤에 `are delicious`를 연결해 비문 | 재표현 승인 후 `Chocolate bars, chocolate ice cream, and chocolate milk are delicious!` 등으로 교체 |
| `sentences[21].exercises.verb.targets[1].cue` | `will not go` | cue가 정답 target `will not go`와 완전히 같아 변형 연습이 성립하지 않음 | 부정 정보를 보존하는 `not / go` 등의 cue와 target 범위를 재설계 |

`come→come`, `grow→grow`, `make→make`처럼 조동사·to 뒤에 원형이 정답인 문항은 cue가 원형이므로 오류로 세지 않았다. 22번은 cue 자체에 양태·부정·본동사 정답이 모두 들어 있어 다르다.

## F-06. 2단계 재표현의 의미 드리프트 (P1, 기존 승인 여부 확인 필요)

`baseText`는 승인된 기존 축약을 보존할 때만 허용된다. 다음은 legacy builder에서 이관된 값이므로 **오류로 단정하지 않고**, 실제 승인 여부를 확인할 검토 대상으로 분리한다.

| JSON 경로 | 드리프트 |
|---|---|
| `sentences[5].exercises.koBlank.baseText` | Mexico/Central America와 `their` 정보 생략 |
| `sentences[8].exercises.koBlank.baseText` | `when ... captured`를 `최초의 탐험가였고 ... 나포했다`로 단순 접속하여 시간 관계 삭제 |
| `sentences[11].exercises.koBlank.baseText` | `the earliest known hot chocolate` 동격어구 생략 |

기존 승인 기록이 없다면 2단계 지시문과 일치하도록 `translation`을 기반으로 재생성하는 것이 안전하다.

## 통과한 항목

- canonical 속 24개 `source`와 `display`는 모두 같고, legacy builder의 `source_sentences` 24개와도 같다.
- 모든 `meaningSegments[].en`을 공백으로 연결하면 해당 `source`가 정확히 복원된다.
- 2·3·5·6·8·10단계 필수 데이터가 모든 24개 문장에 있다. 빈칸 타깃은 `baseText`에서 해석되고, 8단계는 정답 순서로 원문을 정확히 복원한다.
- 어휘 annotation은 문장당 0~3개이고, 영어·한국어 target 쌍이 모두 해석되며, 같은 세그먼트에서 `colorSlot`이 중복되지 않는다.
- 7단계의 5개 오류는 각각 `that`, `made`, `not knowing`, `were added`, `could be drunk`으로 하나의 명확한 수정이 가능하다.
- 9단계 block은 24개 문장을 중복·누락 없이 덮고, `answerOrder=[C,D,A,E,B]`로 원문 1→24번을 복원한다.
- 19번 문장은 번역, 직독직해, 서술어, 어휘, 문장별 정답에서 확정 오류를 찾지 못했다.

## 추측하지 않은 부분

- `Chocolate bars..` 등의 연속 마침표는 legacy 원문과 canonical이 같지만, 선명한 스캔·PDF가 이 감사 범위에 없었다. 따라서 오타로 단정하지 않았고 원문을 바꾸지 않는다.
- `started to become`의 `become`을 strong 범위에 포함할지는 보충어 부정사 판단으로 남겨 두었다.
- 고유명사 표기 `Xocalatl`의 한글 음차 `소칼라틀`은 제공된 자료 밖의 표준 표기를 조회하지 않았으므로 오류 건수에 포함하지 않았다.

## 수정 순서

1. F-02 서술어 annotation과 F-04 단일 정답 선택지를 먼저 고친다.
2. F-01의 의미 단위를 재분할하고, 이에 따라 predicate/vocabulary `segmentId`와 target을 재생성한다.
3. F-03 완성 번역과 연결된 2단계 `koBlank.baseText`를 승인 범위에서 갱신한다.
4. F-05 동사형 문항을 재설계한 뒤 validator를 다시 돌린다.
5. 수정 후 `meaningSegments[].en` 원문 복원, target 해석, 24개 문장 전체 단계 커버리지, HTML/PDF의 strong·어휘 색상을 재검증한다.

## 수정 후 재검증

재검증 결과 **F-01~F-06은 모두 해결**되었고, 남은 사람 판단은 **0건**이다. `sourceStatus.status=confirmed`를 승인된 원문 기준으로 적용했으며 `source`/`display` 24개는 수정하지 않았다.

| 항목 | 상태 | 수정·재검증 결과 |
|---|---|---|
| F-01 직독직해 | 해결 | 24개 문장을 109개 의미 단위로 재구성하고 문장별 `m01`부터 순차 재번호화. 동사+목적어·보어·부사구를 영어 어순으로 분리했으며 모든 `en` 연결이 `source`를 정확히 복원함 |
| F-02 서술어 | 해결 | 서술어 38개를 재연결. `does ... come from`, `can ... make`, `Did ... know`는 분리 target 1개 predicate로 통합했고, 누락된 주절·내포절·관계절 서술어를 추가함. `grow`, 목적 `make`, `Delicious`의 오표시는 제거함 |
| F-03 완성 번역 | 해결 | 9·12·15·18·20·21번의 정보 누락·오역·부자연스러운 표현을 자연스러운 전체 번역으로 교정함 |
| F-04 6단계 | 해결 | 최초 복수 정답 문항 7·8·16·20번을 재설계. 추가로 2·4·9·10·14·16번의 경계적 오답도 주어-동사 일치, to 뒤 원형, 품사, 시제 근거로 명확히 하나만 틀리게 교체. 전체 46개 choice target을 재검토함 |
| F-05 5단계 | 해결 | 1번을 `Chocolate bars, chocolate ice cream, and chocolate milk are delicious!`로 문법적으로 재표현하고 `be→are` 변형을 유지. 22번은 cue를 `not / go (future)`로 바꿔 `will not go`를 그대로 노출하지 않고 미래·부정 변형을 요구함 |
| F-06 2단계 | 해결 | 24개 문항을 모두 완성 `translation`에서 파생하도록 바꾸어 장소·소유·시간 관계·동격어구 생략을 제거. 중복 `baseText`는 저장하지 않으며 모든 빈칸 target이 정본 번역에서 해석됨 |

canonical 최상위 메타데이터도 schema 1.0.0에 맞게 정렬했다. `metadata`는 `title`, `lessonLabel`, 언어 쌍을 포함하고, `sourceStatus`는 출처·확인 시각·legacy SHA-256을 포함하며, `updateState.appliedUpdates`는 `U-20260710-001` object 기록으로 전환했다.

서술어 범위에 대한 기존 유일 판단 항목이었던 7번 `started to become`은, 상태 변화 의미를 실질적으로 담당하는 핵심 보충어로 판단했다. 따라서 `started`와 `become`을 각각 해당 의미 단위에 strong 타깃으로 표시했고 추가 판단 대상을 남기지 않았다.

### 기계 재검증

- `validate_canonical(content, load_spec())`: 오류 **0건**
- `python3 -m unittest discover -s tests -v`: **27/27 통과**
- legacy builder 대비 `source`: **24/24 일치**
- legacy builder 대비 `display`: **24/24 일치**
- `source`+`display` 결합 SHA-256: `754fbe9cd85b57624a295329a833eb609e6afc0537b4f1eca869484f2587a602`
- canonical 전체 SHA-256: `e9d4ba330f82d26f3f265cc5c174098877d18c6827468ef392446c7f54962b7f`
- 기본 문항의 중복 `baseText`: **0개** (`verb` 1번의 승인된 재표현 1건만 `overrideReason`과 함께 유지)
- 남은 사람 판단: **0건**
