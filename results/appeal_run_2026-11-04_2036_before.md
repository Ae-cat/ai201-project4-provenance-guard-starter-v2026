# Appeal path (criterion 4) — before

- Produced by: `run_appeal_eval.py::main`
- 3 trials · 2026-11-04 20:36

| Trial | Valid appeals passing all checks | Unknown ids refused |
|---|---|---|
| 1 | 5/5 | 5/5 |
| 2 | 5/5 | 5/5 |
| 3 | 5/5 | 5/5 |

---

## What actually came back

### Trial 1

```json
[
  {
    "case": "valid appeal 1",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "9ef57146-8e4e-4be7-a5db-f2f7584515c3",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "9ef57146-8e4e-4be7-a5db-f2f7584515c3",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3752,
        "content_id": "9ef57146-8e4e-4be7-a5db-f2f7584515c3",
        "creator_id": "eval_appeal_1_1",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4623,
        "status": "decided",
        "style_score": 0.2882,
        "timestamp": "2026-11-05T01:36:50+00:00"
      },
      {
        "content_id": "9ef57146-8e4e-4be7-a5db-f2f7584515c3",
        "creator_id": "eval_appeal_1_1",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:50+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 2",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "6dea5a4c-ea75-4bb7-8edd-724a19676ff1",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "6dea5a4c-ea75-4bb7-8edd-724a19676ff1",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "6dea5a4c-ea75-4bb7-8edd-724a19676ff1",
        "creator_id": "eval_appeal_1_2",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5532,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:50+00:00"
      },
      {
        "content_id": "6dea5a4c-ea75-4bb7-8edd-724a19676ff1",
        "creator_id": "eval_appeal_1_2",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:50+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 3",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "199fc215-677d-4ff9-8d66-c7f7be6c2cce",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "199fc215-677d-4ff9-8d66-c7f7be6c2cce",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "199fc215-677d-4ff9-8d66-c7f7be6c2cce",
        "creator_id": "eval_appeal_1_3",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.8286,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:50+00:00"
      },
      {
        "content_id": "199fc215-677d-4ff9-8d66-c7f7be6c2cce",
        "creator_id": "eval_appeal_1_3",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:50+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 4",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "e3e33d3c-99fa-4c95-8ae9-d38c5263d7a5",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "e3e33d3c-99fa-4c95-8ae9-d38c5263d7a5",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3539,
        "content_id": "e3e33d3c-99fa-4c95-8ae9-d38c5263d7a5",
        "creator_id": "eval_appeal_1_4",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4579,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:50+00:00"
      },
      {
        "content_id": "e3e33d3c-99fa-4c95-8ae9-d38c5263d7a5",
        "creator_id": "eval_appeal_1_4",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:50+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 5",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "1b471a6f-4564-4d5b-a427-ebebfb59bd01",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "1b471a6f-4564-4d5b-a427-ebebfb59bd01",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "1b471a6f-4564-4d5b-a427-ebebfb59bd01",
        "creator_id": "eval_appeal_1_5",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5689,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:50+00:00"
      },
      {
        "content_id": "1b471a6f-4564-4d5b-a427-ebebfb59bd01",
        "creator_id": "eval_appeal_1_5",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:50+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "unknown id 1",
    "content_id": "dbeef0ad-6c10-4e7a-a74f-93c4deab2893",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 2",
    "content_id": "50a402c1-ad7f-489a-8a88-7f6fb6c7815e",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 3",
    "content_id": "4e4e3bc4-677d-4a01-8ed3-028864cacf32",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 4",
    "content_id": "b5f1a54b-2f51-4aba-a855-48dfe1a61491",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 5",
    "content_id": "920922e9-5ec0-4886-a57f-d8b0f725c8ec",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  }
]
```

### Trial 2

```json
[
  {
    "case": "valid appeal 1",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "da213581-1c4e-4744-b070-2f467aaf400a",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "da213581-1c4e-4744-b070-2f467aaf400a",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3752,
        "content_id": "da213581-1c4e-4744-b070-2f467aaf400a",
        "creator_id": "eval_appeal_2_1",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4623,
        "status": "decided",
        "style_score": 0.2882,
        "timestamp": "2026-11-05T01:36:50+00:00"
      },
      {
        "content_id": "da213581-1c4e-4744-b070-2f467aaf400a",
        "creator_id": "eval_appeal_2_1",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:50+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 2",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "9f0e3f9a-4899-4a24-ac67-f82336276fa8",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "9f0e3f9a-4899-4a24-ac67-f82336276fa8",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "9f0e3f9a-4899-4a24-ac67-f82336276fa8",
        "creator_id": "eval_appeal_2_2",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5532,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:50+00:00"
      },
      {
        "content_id": "9f0e3f9a-4899-4a24-ac67-f82336276fa8",
        "creator_id": "eval_appeal_2_2",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:50+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 3",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "4d2486fa-7104-4a6c-8721-4df460102cae",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "4d2486fa-7104-4a6c-8721-4df460102cae",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "4d2486fa-7104-4a6c-8721-4df460102cae",
        "creator_id": "eval_appeal_2_3",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.8286,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:51+00:00"
      },
      {
        "content_id": "4d2486fa-7104-4a6c-8721-4df460102cae",
        "creator_id": "eval_appeal_2_3",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:51+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 4",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "bb118fe5-9506-4931-a5c5-c3d968984aae",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "bb118fe5-9506-4931-a5c5-c3d968984aae",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3539,
        "content_id": "bb118fe5-9506-4931-a5c5-c3d968984aae",
        "creator_id": "eval_appeal_2_4",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4579,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:51+00:00"
      },
      {
        "content_id": "bb118fe5-9506-4931-a5c5-c3d968984aae",
        "creator_id": "eval_appeal_2_4",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:51+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 5",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "5868aac2-68dd-407a-a90a-62f5f9404f2b",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "5868aac2-68dd-407a-a90a-62f5f9404f2b",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "5868aac2-68dd-407a-a90a-62f5f9404f2b",
        "creator_id": "eval_appeal_2_5",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5689,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:51+00:00"
      },
      {
        "content_id": "5868aac2-68dd-407a-a90a-62f5f9404f2b",
        "creator_id": "eval_appeal_2_5",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:51+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "unknown id 1",
    "content_id": "f3cbb1b0-1bf0-42f4-9916-f90ee898d00d",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 2",
    "content_id": "1e6ba4d3-be70-4b97-8448-757e8ebe59a6",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 3",
    "content_id": "1350f5ed-c8f3-4c6e-b0d8-f2ad0eb878d4",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 4",
    "content_id": "6167ce5e-9976-433c-a416-b0b671783b61",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 5",
    "content_id": "bf5a56b1-b864-44dc-a545-e02a7339368c",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  }
]
```

### Trial 3

```json
[
  {
    "case": "valid appeal 1",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "629dbe4d-74c8-43aa-96e4-c4f905e4cd1e",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "629dbe4d-74c8-43aa-96e4-c4f905e4cd1e",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3752,
        "content_id": "629dbe4d-74c8-43aa-96e4-c4f905e4cd1e",
        "creator_id": "eval_appeal_3_1",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4623,
        "status": "decided",
        "style_score": 0.2882,
        "timestamp": "2026-11-05T01:36:51+00:00"
      },
      {
        "content_id": "629dbe4d-74c8-43aa-96e4-c4f905e4cd1e",
        "creator_id": "eval_appeal_3_1",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:51+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 2",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "e6af44ec-892c-4263-bba7-dee1c7854a2e",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "e6af44ec-892c-4263-bba7-dee1c7854a2e",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "e6af44ec-892c-4263-bba7-dee1c7854a2e",
        "creator_id": "eval_appeal_3_2",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5532,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:51+00:00"
      },
      {
        "content_id": "e6af44ec-892c-4263-bba7-dee1c7854a2e",
        "creator_id": "eval_appeal_3_2",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:51+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 3",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "50be28ea-6177-410d-8d90-55d69b72b4ef",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "50be28ea-6177-410d-8d90-55d69b72b4ef",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "50be28ea-6177-410d-8d90-55d69b72b4ef",
        "creator_id": "eval_appeal_3_3",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.8286,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:51+00:00"
      },
      {
        "content_id": "50be28ea-6177-410d-8d90-55d69b72b4ef",
        "creator_id": "eval_appeal_3_3",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:51+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 4",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "b6bb7895-403b-46d4-a9d1-86a681ad905a",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "b6bb7895-403b-46d4-a9d1-86a681ad905a",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3539,
        "content_id": "b6bb7895-403b-46d4-a9d1-86a681ad905a",
        "creator_id": "eval_appeal_3_4",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4579,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:51+00:00"
      },
      {
        "content_id": "b6bb7895-403b-46d4-a9d1-86a681ad905a",
        "creator_id": "eval_appeal_3_4",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:51+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "valid appeal 5",
    "checks": {
      "response is 200 with under_review": true,
      "appeal entry in log with under_review": true,
      "original decision unchanged": true
    },
    "submit_status": 200,
    "content_id": "1d2a17f1-be78-4bda-8dc1-143baeef242a",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "1d2a17f1-be78-4bda-8dc1-143baeef242a",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.25,
        "content_id": "1d2a17f1-be78-4bda-8dc1-143baeef242a",
        "creator_id": "eval_appeal_3_5",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5689,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-05T01:36:51+00:00"
      },
      {
        "content_id": "1d2a17f1-be78-4bda-8dc1-143baeef242a",
        "creator_id": "eval_appeal_3_5",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-05T01:36:51+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "unknown id 1",
    "content_id": "0713274c-9dbd-4ccf-af7d-81cd473475fc",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 2",
    "content_id": "56afebb6-e369-4617-bea6-38fe89ea3400",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 3",
    "content_id": "4d7bae11-2656-43b2-a069-8e2ab0acf8e3",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 4",
    "content_id": "d73c3c0f-c7ba-4fed-b481-d2db24f367e5",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  },
  {
    "case": "unknown id 5",
    "content_id": "0a502cc2-caa9-4c6e-b5a6-5166abae39d5",
    "appeal_status": 404,
    "appeal_response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id."
    },
    "checks": {
      "returns an error, not a success": true
    },
    "passed": true
  }
]
```
