# ShelfScanApp API�݌v��(GAS)

## 1. �G���h�|�C���g
   Google Apps Script WebApp URL�i��j�F
   https://script.google.com/macros/s/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/exec


## 2. ���ʎd�l
### 2.1 HTTP���\�b�h�FGET / POST�i�p�r�ɉ����đI���j
### 2.2 Content-Type
- GET�Fapplication/x-www-form-urlencoded
- POST�Fapplication/json
### 2.3 ���ʃp�����[�^�F
- action�istring�j�F���s���鏈�����
- ���̑��̃p�����[�^�� action �ɉ����đ��M


## 3. �A�N�V�����ʎd�l
### 3.1 �ꗗ�擾
- action�Flist
- ���\�b�h�FGET
- �p�����[�^�F
- status�istring, �C�Ӂj�F"pending" �̂ݎ擾����ꍇ�Ɏw��
- �������e�FGoogle Spreadsheet ����w���\��i�ꗗ���擾���AJSON�z��Ƃ��ĕԋp
- ���X�|���X��F
```json
    [
      { "id": "1", "name": "���iA", "price": 1200, "deadline": "2025-08-23", "status": "pending" },
      { "id": "2", "name": "���iB", "price": 500, "deadline": "2025-08-15", "status": "done" }
    ]
```
   ### 3.2 �V�K�o�^
- action�Fadd
- ���\�b�h�FPOST
- ���N�G�X�g�{�f�B�F
```json
    {
      "name": "���iA",
      "price": 1200,
      "deadline": "2025-08-23"
    }
```
- �������e�FSpreadsheet �ɐV�K�s��ǉ��iID�͎����̔ԁj
- ���X�|���X��F
```json
    { "result": "success", "id": "3" }
```

### 3.3 �X�e�[�^�X�X�V
- action�Fupdate
- ���\�b�h�FPOST
- ���N�G�X�g�{�f�B�F
```json
    {
      "id": "3",
      "status": "done"
    }
```
- �������e�F�Y�� ID �̍s���������Astatus ���X�V
- ���X�|���X��F
```json
    { "result": "success" }
```

### 3.4 �폜
- action�Fdelete
- ���\�b�h�FPOST
- ���N�G�X�g�{�f�B�F
```json
    {
      "id": "3"
    }
```
- �������e�F�Y�� ID �̍s���폜
- ���X�|���X��F
```json
    { "result": "success" }
```


## 4. �G���[���X�|���X��
```json
   { "result": "error", "message": "Item not found" }
```


## 5. ���l
### 5.1 Spreadsheet �\����
| ID | �i��   | ���i  | ����         | �X�e�[�^�X
| -- | ------ | ----- | ------------ | ----------
| 1  | ���iA  | 1200  | 2025-08-23   | pending
| 2  | ���iB  | 500   | 2025-08-15   | done
