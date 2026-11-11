import unittest
from check_response_format import check_response

TABLE = '|环节|说明|\n|---|---|\n|边界|只说明一次|'
TEACH = '### 结论\n结论。\n\n### 机制\n' + TABLE + '\n\n### 验证\n这个判断成立吗？'
CLOSE = '### 状态\n未保存。\n\n### 记录\n' + TABLE + '\n\n### 入口\n权限未通过，无新记录入口。'


class ResponseEnvelopeTest(unittest.TestCase):
    def test_valid_teach_and_close(self):
        self.assertEqual(check_response(TEACH, 'teach'), [])
        self.assertEqual(check_response(CLOSE, 'close'), [])

    def test_intro_and_separate_material_paragraph_rejected(self):
        self.assertTrue(check_response('我来讲一下。\n\n' + TEACH, 'teach'))
        self.assertTrue(check_response(TEACH.replace(TABLE, TABLE + '\n\n教材入口另列。'), 'teach'))

    def test_duplicate_table_and_extra_heading_rejected(self):
        self.assertTrue(check_response(TEACH.replace(TABLE, TABLE + '\n\n' + TABLE), 'teach'))
        self.assertTrue(check_response(TEACH + '\n\n### 修法\n再讲一段', 'teach'))

    def test_code_and_question_share_final_section(self):
        text = TEACH.replace('这个判断成立吗？', '```js\nconst n = 1;\n```\n这个判断成立吗？')
        self.assertEqual(check_response(text, 'teach'), [])
        text = TEACH.replace('这个判断成立吗？', '```js\n' + 'x();\n' * 7 + '```\n结果是什么？')
        self.assertTrue(check_response(text, 'teach'))

    def test_internal_ids_and_levels_are_not_learner_labels(self):
        self.assertTrue(check_response(TEACH.replace('结论。', 'fe.web.lifecycle是L2。'), 'teach'))
        self.assertEqual(check_response(TEACH.replace('结论。', '[真实标题](/repo/fe.web.lifecycle.md:5)。'), 'teach'), [])

    def test_empty_middle_and_extra_paragraph_rejected(self):
        self.assertTrue(check_response(TEACH.replace(TABLE, ''), 'teach'))
        self.assertTrue(check_response(TEACH + '\n\n再追加一句。', 'teach'))

    def test_flow_is_one_line_with_at_most_four_steps(self):
        self.assertEqual(check_response(TEACH.replace(TABLE, '读取 → 校验 → 提交'), 'teach'), [])
        self.assertTrue(check_response(TEACH.replace(TABLE, 'A → B → C → D → E'), 'teach'))
