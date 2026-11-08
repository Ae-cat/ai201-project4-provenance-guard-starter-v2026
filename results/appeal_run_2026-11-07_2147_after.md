# Appeal path (criterion 4) — after

- Produced by: `run_appeal_eval.py::main`
- 3 trials · 2026-11-07 21:47

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
    "content_id": "b2218ba5-ca9d-475d-9931-11af97c5be1a",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "b2218ba5-ca9d-475d-9931-11af97c5be1a",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3752,
        "content_id": "b2218ba5-ca9d-475d-9931-11af97c5be1a",
        "creator_id": "eval_appeal_1_1",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4623,
        "status": "decided",
        "style_score": 0.2882,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "b2218ba5-ca9d-475d-9931-11af97c5be1a",
        "creator_id": "eval_appeal_1_1",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "465538e1-0602-4847-aa7d-fedceb97ecdb",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "465538e1-0602-4847-aa7d-fedceb97ecdb",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.4016,
        "content_id": "465538e1-0602-4847-aa7d-fedceb97ecdb",
        "creator_id": "eval_appeal_1_2",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5532,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "465538e1-0602-4847-aa7d-fedceb97ecdb",
        "creator_id": "eval_appeal_1_2",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "d3266618-6d0a-4009-808e-a555cc582b5f",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "d3266618-6d0a-4009-808e-a555cc582b5f",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.5393,
        "content_id": "d3266618-6d0a-4009-808e-a555cc582b5f",
        "creator_id": "eval_appeal_1_3",
        "guess": "unsure",
        "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
        "model_score": 0.8286,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "d3266618-6d0a-4009-808e-a555cc582b5f",
        "creator_id": "eval_appeal_1_3",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "4d7efb3e-e7bd-4c09-89f7-70a4a2fc85d9",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "4d7efb3e-e7bd-4c09-89f7-70a4a2fc85d9",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3539,
        "content_id": "4d7efb3e-e7bd-4c09-89f7-70a4a2fc85d9",
        "creator_id": "eval_appeal_1_4",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4579,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "4d7efb3e-e7bd-4c09-89f7-70a4a2fc85d9",
        "creator_id": "eval_appeal_1_4",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "40031f93-45c6-443e-8cd3-8b2ad46f1bf0",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "40031f93-45c6-443e-8cd3-8b2ad46f1bf0",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.4094,
        "content_id": "40031f93-45c6-443e-8cd3-8b2ad46f1bf0",
        "creator_id": "eval_appeal_1_5",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5689,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "40031f93-45c6-443e-8cd3-8b2ad46f1bf0",
        "creator_id": "eval_appeal_1_5",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "unknown id 1",
    "content_id": "14dccc48-da55-4ac9-a69f-9ac2cfb4ece4",
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
    "content_id": "271399a2-e9d3-4a1a-948a-5b5e1d5bb440",
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
    "content_id": "b6c8baae-8e30-4e99-896d-41e9bd217c1b",
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
    "content_id": "257baf09-bf91-4bca-8d7e-9fda330bb0d3",
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
    "content_id": "b53d2821-433c-40ae-92a4-2a3995691e8b",
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
    "content_id": "84a317f5-7e98-4829-b79e-7ef87edbee25",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "84a317f5-7e98-4829-b79e-7ef87edbee25",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3752,
        "content_id": "84a317f5-7e98-4829-b79e-7ef87edbee25",
        "creator_id": "eval_appeal_2_1",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4623,
        "status": "decided",
        "style_score": 0.2882,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "84a317f5-7e98-4829-b79e-7ef87edbee25",
        "creator_id": "eval_appeal_2_1",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "8de27492-5c57-4466-8371-834b330cb023",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "8de27492-5c57-4466-8371-834b330cb023",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.4016,
        "content_id": "8de27492-5c57-4466-8371-834b330cb023",
        "creator_id": "eval_appeal_2_2",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5532,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "8de27492-5c57-4466-8371-834b330cb023",
        "creator_id": "eval_appeal_2_2",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "36652505-8d66-4450-ad78-1fc3d1f88b36",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "36652505-8d66-4450-ad78-1fc3d1f88b36",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.5393,
        "content_id": "36652505-8d66-4450-ad78-1fc3d1f88b36",
        "creator_id": "eval_appeal_2_3",
        "guess": "unsure",
        "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
        "model_score": 0.8286,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "36652505-8d66-4450-ad78-1fc3d1f88b36",
        "creator_id": "eval_appeal_2_3",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "87c3ec0c-5ad8-4174-94e8-ca068f78e034",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "87c3ec0c-5ad8-4174-94e8-ca068f78e034",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3539,
        "content_id": "87c3ec0c-5ad8-4174-94e8-ca068f78e034",
        "creator_id": "eval_appeal_2_4",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4579,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "87c3ec0c-5ad8-4174-94e8-ca068f78e034",
        "creator_id": "eval_appeal_2_4",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "e638833a-6df9-40a2-9587-25daa796c67f",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "e638833a-6df9-40a2-9587-25daa796c67f",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.4094,
        "content_id": "e638833a-6df9-40a2-9587-25daa796c67f",
        "creator_id": "eval_appeal_2_5",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5689,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "e638833a-6df9-40a2-9587-25daa796c67f",
        "creator_id": "eval_appeal_2_5",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "unknown id 1",
    "content_id": "167067ab-114a-44ec-a68a-e3419f225fb0",
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
    "content_id": "cae1376a-15b8-4013-accf-ffc56551e0e6",
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
    "content_id": "7af41c55-96dd-494b-9861-77751161723a",
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
    "content_id": "2767da46-edea-4b8b-b313-43c95c9ad043",
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
    "content_id": "c5c023bd-cd67-4e5e-b15c-f1bf55c40f0f",
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
    "content_id": "3a165a2b-1de5-49ea-8424-eb2f1cf51e31",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "3a165a2b-1de5-49ea-8424-eb2f1cf51e31",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3752,
        "content_id": "3a165a2b-1de5-49ea-8424-eb2f1cf51e31",
        "creator_id": "eval_appeal_3_1",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4623,
        "status": "decided",
        "style_score": 0.2882,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "3a165a2b-1de5-49ea-8424-eb2f1cf51e31",
        "creator_id": "eval_appeal_3_1",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "75e237f0-2b7e-4d41-bf59-b4aadc153eca",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "75e237f0-2b7e-4d41-bf59-b4aadc153eca",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.4016,
        "content_id": "75e237f0-2b7e-4d41-bf59-b4aadc153eca",
        "creator_id": "eval_appeal_3_2",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5532,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "75e237f0-2b7e-4d41-bf59-b4aadc153eca",
        "creator_id": "eval_appeal_3_2",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "223cf771-172f-4f90-b12a-896e55bc473d",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "223cf771-172f-4f90-b12a-896e55bc473d",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.5393,
        "content_id": "223cf771-172f-4f90-b12a-896e55bc473d",
        "creator_id": "eval_appeal_3_3",
        "guess": "unsure",
        "label": "We can't tell whether a person or AI wrote this, or whether AI helped. If you wrote it yourself, please let us know.",
        "model_score": 0.8286,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "223cf771-172f-4f90-b12a-896e55bc473d",
        "creator_id": "eval_appeal_3_3",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "16b4d20f-d4d2-4a92-9842-1d644dc04eff",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "16b4d20f-d4d2-4a92-9842-1d644dc04eff",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.3539,
        "content_id": "16b4d20f-d4d2-4a92-9842-1d644dc04eff",
        "creator_id": "eval_appeal_3_4",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.4579,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "16b4d20f-d4d2-4a92-9842-1d644dc04eff",
        "creator_id": "eval_appeal_3_4",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
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
    "content_id": "7921aef8-6443-42a6-8211-f4fca0047f71",
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "7921aef8-6443-42a6-8211-f4fca0047f71",
      "message": "Thanks. Your appeal has been recorded and this item is now under review.",
      "status": "under_review"
    },
    "log_entries": [
      {
        "combined_score": 0.4094,
        "content_id": "7921aef8-6443-42a6-8211-f4fca0047f71",
        "creator_id": "eval_appeal_3_5",
        "guess": "human",
        "label": "We think this was probably written by a person. If you know it wasn't, please let us know.",
        "model_score": 0.5689,
        "status": "decided",
        "style_score": 0.25,
        "timestamp": "2026-11-08T02:47:29+00:00"
      },
      {
        "content_id": "7921aef8-6443-42a6-8211-f4fca0047f71",
        "creator_id": "eval_appeal_3_5",
        "event": "appeal",
        "reasoning": "I wrote this myself.",
        "status": "under_review",
        "timestamp": "2026-11-08T02:47:29+00:00"
      }
    ],
    "passed": true
  },
  {
    "case": "unknown id 1",
    "content_id": "910206e0-0923-4d25-a50f-c9387a21f3ab",
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
    "content_id": "999f9292-bf86-434d-8688-43b02bd393c9",
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
    "content_id": "5b0e445d-269e-4bbe-8768-c8607bb5408c",
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
    "content_id": "57a409ca-0947-4292-b42f-822aabae7ff7",
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
    "content_id": "9e63ed18-f3ba-4a8f-80c9-7a14ea4d1b62",
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
