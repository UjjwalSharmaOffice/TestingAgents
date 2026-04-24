import json

data = {
  "project": "CodEval Platform",
  "scope": "Team 1 (Authentication + Admin Platform) and Team 1 + Team 2 Combined (Integration Contracts)",
  "generated_at": "2026-04-22",
  "features": [
    {
      "epic_id": "E1",
      "feature": "User Login with EPAM company email and password",
      "qa_story": {
        "title": "As a registered and authorized EPAM staff member, I should be able to log in using my EPAM company email and correct password so that access is restricted to authorized EPAM staff",
        "acceptance_criteria": [
          "Email field validates @epam.com domain only — other domains are blocked at input level",
          "On valid credentials: JWT is issued with the correct role (ADMIN or USER) and stored in an HttpOnly cookie",
          "ADMIN token has an 8-hour expiry and redirects to the Admin Dashboard",
          "USER token has a 4-hour expiry and redirects to the User Dashboard",
          "On invalid credentials: an inline error is shown with no account enumeration message",
          "RBAC middleware (isAdmin / isUser) is applied at the route level on all protected endpoints"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-E1-01",
          "title": "Successful login as USER redirects to User Dashboard with correct JWT",
          "steps": [
            "Navigate to the Login Page",
            "Enter a valid @epam.com email belonging to a USER-role account",
            "Enter the correct password",
            "Click the Login button"
          ],
          "expected_result": "JWT issued with role=USER and 4-hour expiry, stored in HttpOnly cookie; user redirected to User Dashboard"
        },
        {
          "id": "TS-E1-02",
          "title": "Successful login as ADMIN redirects to Admin Dashboard with correct JWT",
          "steps": [
            "Navigate to the Login Page",
            "Enter a valid @epam.com email belonging to an ADMIN-role account",
            "Enter the correct password",
            "Click the Login button"
          ],
          "expected_result": "JWT issued with role=ADMIN and 8-hour expiry, stored in HttpOnly cookie; user redirected to Admin Dashboard"
        },
        {
          "id": "TS-E1-03",
          "title": "Login with non-@epam.com email is blocked at input level",
          "steps": [
            "Navigate to the Login Page",
            "Enter an email with a domain other than @epam.com",
            "Attempt to proceed"
          ],
          "expected_result": "Input blocked at field level; user cannot proceed with non-@epam.com email"
        },
        {
          "id": "TS-E1-04",
          "title": "Login with invalid credentials shows inline error without account enumeration",
          "steps": [
            "Navigate to the Login Page",
            "Enter a valid @epam.com email",
            "Enter an incorrect password",
            "Click the Login button"
          ],
          "expected_result": "Inline error displayed that does not reveal whether email or password is incorrect"
        }
      ],
      "edge_cases": [
        {
          "description": "Non-@epam.com domain email entered in the email field",
          "expected_behavior": "Blocked at input level per @epam.com domain validation rule"
        },
        {
          "description": "USER role JWT used to access an ADMIN-only route",
          "expected_behavior": "RBAC middleware denies access; Access Denied page shown"
        },
        {
          "description": "ADMIN role JWT used to access a USER-only route",
          "expected_behavior": "RBAC middleware denies access; Access Denied page shown"
        }
      ]
    },
    {
      "epic_id": "E1",
      "feature": "New platform user signup with EPAM email",
      "qa_story": {
        "title": "As a new platform user, I should be able to sign up using a valid EPAM email and a secure password so that I can create an account",
        "acceptance_criteria": [
          "Signup form fields: email (@epam.com), name, password, confirm password",
          "Password rules enforced on frontend and backend: min 8 characters, 1 uppercase, 1 number, 1 special character",
          "Duplicate email returns message 'Account already exists' with a login link",
          "Default role assigned is USER unless overridden by an admin",
          "On successful signup: user redirected to the appropriate dashboard based on role"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-E1-05",
          "title": "Successful signup with valid @epam.com email and compliant password",
          "steps": [
            "Navigate to the Signup Page",
            "Enter a valid @epam.com email",
            "Enter a name",
            "Enter a password meeting all strength rules",
            "Re-enter same password in confirm password",
            "Submit the form"
          ],
          "expected_result": "Account created with role=USER; user redirected to User Dashboard"
        },
        {
          "id": "TS-E1-06",
          "title": "Signup with already-registered email shows 'Account already exists' with login link",
          "steps": [
            "Navigate to the Signup Page",
            "Enter an @epam.com email that is already registered",
            "Complete remaining fields with valid data",
            "Submit the form"
          ],
          "expected_result": "Error 'Account already exists' displayed with a link to the Login page"
        },
        {
          "id": "TS-E1-07",
          "title": "Signup with password not meeting strength rules is rejected",
          "steps": [
            "Navigate to the Signup Page",
            "Enter valid email and name",
            "Enter a password that fails one or more strength rules",
            "Submit the form"
          ],
          "expected_result": "Frontend and backend validation prevents account creation; strength error displayed"
        }
      ],
      "edge_cases": [
        {
          "description": "Non-@epam.com domain email entered in signup",
          "expected_behavior": "Blocked per @epam.com domain validation"
        },
        {
          "description": "Confirm password does not match the password field",
          "expected_behavior": "Form submission blocked; password mismatch error shown"
        }
      ]
    },
    {
      "epic_id": "E1",
      "feature": "Password reset via email for any platform user",
      "qa_story": {
        "title": "As a user who has forgotten their password, I should be able to request a password reset using their registered email and set a new password so that they can regain access to the platform",
        "acceptance_criteria": [
          "Forgot Password page accepts email input and sends a reset link expiring in 15 minutes",
          "Reset link is single-use and HMAC-signed with userId and expiry",
          "Reset Password page requires new password and confirm password validated against same strength rules as signup",
          "On successful reset: all active sessions for that user are invalidated via Redis revocation list",
          "Access Denied page shown when a user attempts to access an unauthorised route"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-E1-08",
          "title": "Successful password reset with valid registered email",
          "steps": [
            "Navigate to the Forgot Password page",
            "Enter a registered @epam.com email",
            "Submit the form",
            "Click reset link within 15 minutes",
            "Enter new password and confirm password meeting strength rules",
            "Submit the Reset Password form"
          ],
          "expected_result": "Password updated; all active sessions invalidated via Redis; user redirected appropriately"
        },
        {
          "id": "TS-E1-09",
          "title": "Expired or already-used reset link is rejected",
          "steps": [
            "Obtain a password reset link",
            "Use the link once or wait past the 15-minute expiry",
            "Attempt to use the same link again"
          ],
          "expected_result": "Reset link rejected as single-use or expired"
        },
        {
          "id": "TS-E1-10",
          "title": "Access Denied page shown when accessing an unauthorised route",
          "steps": [
            "Attempt to navigate to a route requiring a role not in the current JWT"
          ],
          "expected_result": "Access Denied page displayed"
        }
      ],
      "edge_cases": [
        {
          "description": "Reset link accessed at the 15-minute expiry boundary",
          "expected_behavior": "Link treated as expired and rejected"
        },
        {
          "description": "New password on Reset page does not meet strength rules",
          "expected_behavior": "Password update blocked; strength validation error displayed"
        }
      ]
    },
    {
      "epic_id": "A-E1",
      "feature": "Admin views paginated and filterable list of all users (A-1.1)",
      "qa_story": {
        "title": "As an admin, I should be able to view a paginated, filterable list of all users so that I can manage the users",
        "acceptance_criteria": [
          "Columns: name, email, role, isActive, createdAt, batches, total assessments",
          "Filter by: role, isActive status, batch",
          "Full-text search on name and email with 300ms debounce",
          "Pagination defaults to 20 users per page and is configurable"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A1-01",
          "title": "Admin opens User Management page and sees default paginated list with all required columns",
          "steps": [
            "Log in as an admin",
            "Navigate to the User Management page"
          ],
          "expected_result": "User list displayed with columns: name, email, role, isActive, createdAt, batches, total assessments; defaults to 20 per page"
        },
        {
          "id": "TS-A1-02",
          "title": "Admin filters list by role, isActive, and batch",
          "steps": [
            "On User Management page, apply filter by role",
            "Apply filter by isActive",
            "Apply filter by batch"
          ],
          "expected_result": "User list updates to show only users matching each applied filter"
        },
        {
          "id": "TS-A1-03",
          "title": "Admin searches users by name and email with 300ms debounce",
          "steps": [
            "On User Management page, type in the search field"
          ],
          "expected_result": "After 300ms debounce, list updates to show matching users"
        }
      ],
      "edge_cases": [
        {
          "description": "Admin configures pagination to a non-default page size",
          "expected_behavior": "User list displays configured number of users per page"
        }
      ]
    },
    {
      "epic_id": "A-E1",
      "feature": "Admin views individual user details and performance statistics (A-1.2)",
      "qa_story": {
        "title": "As an admin, I should be able to view an individual user's details and performance statistics so that I can evaluate their history",
        "acceptance_criteria": [
          "Detail view: name, email, role, status, createdAt, batch memberships",
          "Statistics: total assessments assigned, attempted, average score, best score",
          "Assessment history table is read-only and reads from the results API"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A1-04",
          "title": "Admin opens user detail view and sees all required fields and read-only history",
          "steps": [
            "Navigate to User Management page",
            "Click on a user to open detail view"
          ],
          "expected_result": "Detail view shows name, email, role, status, createdAt, batch memberships, statistics section, and read-only history table"
        }
      ],
      "edge_cases": [
        {
          "description": "User has no assessment history",
          "expected_behavior": "Statistics show zero/empty values; history table is empty"
        }
      ]
    },
    {
      "epic_id": "A-E1",
      "feature": "Admin creates, edits, and deactivates user accounts (A-1.3)",
      "qa_story": {
        "title": "As an admin, I should be able to create, edit, and deactivate user accounts so that the user database stays accurate",
        "acceptance_criteria": [
          "Create: name + email required; role auto-assigned as USER",
          "Edit: name, role, isActive toggle",
          "Deactivate (soft delete): sets isActive=false, immediately invalidates all active sessions",
          "Deactivated user data retained for historical reporting"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A1-05",
          "title": "Admin creates new user with name and email; role auto-assigned as USER",
          "steps": [
            "Navigate to User Management page",
            "Open create user form",
            "Enter valid name and @epam.com email",
            "Submit"
          ],
          "expected_result": "User created with role=USER; appears in user list"
        },
        {
          "id": "TS-A1-06",
          "title": "Admin deactivates user; isActive=false and all sessions immediately invalidated",
          "steps": [
            "Open detail view of an active user",
            "Toggle isActive to deactivate",
            "Confirm"
          ],
          "expected_result": "isActive=false; all active sessions immediately invalidated; data retained"
        },
        {
          "id": "TS-A1-07",
          "title": "Admin edits user name, role, and isActive toggle",
          "steps": [
            "Open edit form for a user",
            "Update name, role, isActive",
            "Save"
          ],
          "expected_result": "User record updated with new values"
        }
      ],
      "edge_cases": [
        {
          "description": "Deactivated user historical data",
          "expected_behavior": "Retained and accessible for reporting after deactivation"
        }
      ]
    },
    {
      "epic_id": "A-E1",
      "feature": "Admin creates and manages batches with user assignment (A-1.4)",
      "qa_story": {
        "title": "As an admin, I should be able to create and manage batches and assign users to them so that I can send invites to assessments efficiently",
        "acceptance_criteria": [
          "Batch fields: name, description, createdBy",
          "Members added individually or via CSV bulk-upload (email column)",
          "Members can be removed from batch",
          "User can belong to multiple batches; no duplicate members (BatchMembers unique constraint)",
          "Batch detail: member count, assessments assigned, avg group score"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A1-08",
          "title": "Admin creates a batch and verifies detail view",
          "steps": [
            "Navigate to Batch Management page",
            "Open create batch form",
            "Enter name and description",
            "Submit"
          ],
          "expected_result": "Batch created; detail view shows member count, assessments assigned, avg group score"
        },
        {
          "id": "TS-A1-09",
          "title": "Admin adds users to batch via CSV bulk-upload",
          "steps": [
            "Navigate to batch detail page",
            "Upload CSV with email column"
          ],
          "expected_result": "Valid users from CSV added to batch"
        },
        {
          "id": "TS-A1-10",
          "title": "Adding duplicate member to batch is prevented",
          "steps": [
            "Attempt to add a user already in the batch"
          ],
          "expected_result": "Duplicate not added; BatchMembers unique constraint enforced"
        }
      ],
      "edge_cases": [
        {
          "description": "User belonging to multiple batches",
          "expected_behavior": "Appears in each batch independently without conflict"
        }
      ]
    },
    {
      "epic_id": "A-E3",
      "feature": "Admin creates and configures assessment with questions, duration, attempts, scoring rules (A-3.1)",
      "qa_story": {
        "title": "As an admin, I should be able to create and configure an assessment with questions, duration, attempts, and scoring rules so that assessments can be set up independently of inviting candidates",
        "acceptance_criteria": [
          "Fields: title, description, duration (minutes), startTime, endTime, maxAttempts, status",
          "Add questions from bank with marks (AssessmentQuestions.marks) and orderIndex",
          "Scoring rules: weighted or equal per question",
          "Assessment saved in DRAFT status until invites are sent"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A3-01",
          "title": "Admin creates fully configured assessment saved as DRAFT",
          "steps": [
            "Navigate to Assessment Management page",
            "Open create form",
            "Fill all fields and add questions with marks and orderIndex",
            "Configure scoring rules",
            "Save"
          ],
          "expected_result": "Assessment created with status=DRAFT; all fields persisted"
        },
        {
          "id": "TS-A3-02",
          "title": "Admin configures weighted scoring rules per question",
          "steps": [
            "Open a DRAFT assessment",
            "Set scoring rule to weighted",
            "Assign marks to each question",
            "Save"
          ],
          "expected_result": "Weighted rules and marks saved correctly"
        }
      ],
      "edge_cases": [
        {
          "description": "Assessment saved without sending invites",
          "expected_behavior": "Remains in DRAFT status until invites explicitly sent"
        }
      ]
    },
    {
      "epic_id": "A-E3",
      "feature": "Admin selects users or batch and triggers assessment invite emails (A-3.2)",
      "qa_story": {
        "title": "As an admin, I should be able to select users or a batch to invite and trigger assessment invite emails so that candidates are notified with their unique access links",
        "acceptance_criteria": [
          "Selection popup: search and multi-select of individuals or whole batches",
          "Preview list of invitees shown before sending",
          "Per-candidate HMAC-signed token generated with configurable expiry",
          "Email dispatched async with assessment link and instructions",
          "Assessment status moves to ACTIVE after sending",
          "Per-candidate invite status visible: PENDING / SENT / OPENED"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A3-03",
          "title": "Admin selects invitees, previews list, sends; assessment moves to ACTIVE",
          "steps": [
            "Open DRAFT assessment and go to Send Invites",
            "Search and multi-select users or whole batch",
            "Review preview list",
            "Confirm and send"
          ],
          "expected_result": "Emails dispatched async with HMAC-signed links; assessment moves to ACTIVE; per-candidate status shown as PENDING/SENT"
        },
        {
          "id": "TS-A3-04",
          "title": "Admin monitors per-candidate invite status",
          "steps": [
            "Navigate to invite status view for an ACTIVE assessment"
          ],
          "expected_result": "Per-candidate status displayed as PENDING, SENT, or OPENED"
        }
      ],
      "edge_cases": [
        {
          "description": "Whole batch invited with multiple users",
          "expected_behavior": "Each user receives individual HMAC-signed link"
        }
      ]
    },
    {
      "epic_id": "A-E3",
      "feature": "Admin views, edits, and deletes assessments (A-3.3)",
      "qa_story": {
        "title": "As an admin, I should be able to view, edit, and delete assessments so that I can manage the full assessment lifecycle",
        "acceptance_criteria": [
          "List: title, status, startTime, endTime, candidate count, avg score",
          "Filter by status (DRAFT/ACTIVE/COMPLETED) and date range",
          "Edit blocked when status=ACTIVE and candidates have started",
          "Delete is soft-delete only; blocked if UserAssessments records exist"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A3-05",
          "title": "Admin views assessment list and applies status and date range filters",
          "steps": [
            "Navigate to Assessment Management page",
            "Apply status and date range filters"
          ],
          "expected_result": "List shows only matching assessments"
        },
        {
          "id": "TS-A3-06",
          "title": "Edit blocked on ACTIVE assessment where candidates have started",
          "steps": [
            "Open ACTIVE assessment where a candidate started",
            "Attempt to edit"
          ],
          "expected_result": "Edit action blocked"
        },
        {
          "id": "TS-A3-07",
          "title": "Soft-delete blocked when UserAssessments records exist",
          "steps": [
            "Open assessment with existing UserAssessments records",
            "Attempt to delete"
          ],
          "expected_result": "Delete blocked due to existing UserAssessments records"
        }
      ],
      "edge_cases": [
        {
          "description": "Assessment in DRAFT with no UserAssessments records",
          "expected_behavior": "Edit and soft-delete both permitted"
        }
      ]
    },
    {
      "epic_id": "A-E3",
      "feature": "Admin resends assessment invite to candidates with PENDING status (A-3.4)",
      "qa_story": {
        "title": "As an admin, I should be able to send an email to invite users to an existing assessment or resend to those who missed the email so that all intended candidates receive their access links",
        "acceptance_criteria": [
          "Can send to new users not in original invite",
          "Resend available only when candidate status is PENDING"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A3-08",
          "title": "Admin resends invite to candidate with PENDING status",
          "steps": [
            "Navigate to invite status page for ACTIVE assessment",
            "Locate candidate with status=PENDING",
            "Trigger resend"
          ],
          "expected_result": "Invite email resent to candidate"
        },
        {
          "id": "TS-A3-09",
          "title": "Resend unavailable for candidates not in PENDING status",
          "steps": [
            "Locate candidate with status=SENT or OPENED",
            "Attempt resend"
          ],
          "expected_result": "Resend option not available for non-PENDING candidates"
        }
      ],
      "edge_cases": [
        {
          "description": "Candidate transitions from PENDING to SENT between page load and resend action",
          "expected_behavior": "Resend only executed if status still PENDING at request time"
        }
      ]
    },
    {
      "epic_id": "A-E2",
      "feature": "Admin triggers AI-based question generation with configurable parameters (A-2.1)",
      "qa_story": {
        "title": "As an admin, I should be able to trigger AI-based question generation with parameters so that coding questions are created automatically without manual writing",
        "acceptance_criteria": [
          "Parameters: difficulty (Easy/Med/Hard), topic, subTopic, count (1-10), include test cases toggle",
          "Spring AI calls LLM with fixed internal system prompt not visible to admin",
          "Streaming response displayed in editor as it arrives",
          "Output: title, description, constraints, sample code, test cases",
          "On failure: retry once; if still failing, error with 'Try Again' button shown"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A2-01",
          "title": "Admin triggers AI generation and receives streamed output with all required fields",
          "steps": [
            "Navigate to Question Management page",
            "Set parameters: difficulty, topic, subTopic, count, include test cases",
            "Trigger generation"
          ],
          "expected_result": "Streaming response shown in editor; output contains title, description, constraints, sample code, test cases"
        },
        {
          "id": "TS-A2-02",
          "title": "AI generation failure triggers one retry; if fails again shows Try Again button",
          "steps": [
            "Trigger AI generation in a failing state",
            "Observe system behaviour"
          ],
          "expected_result": "System retries once; if retry fails, error shown with Try Again button"
        }
      ],
      "edge_cases": [
        {
          "description": "Count set to boundary minimum: 1",
          "expected_behavior": "Exactly one question generated"
        },
        {
          "description": "Count set to boundary maximum: 10",
          "expected_behavior": "Up to ten questions generated"
        }
      ]
    },
    {
      "epic_id": "A-E2",
      "feature": "Admin reviews and edits AI-generated questions in code editor before publishing (A-2.2)",
      "qa_story": {
        "title": "As an admin, I should be able to review and edit AI-generated questions in the code editor before publishing so that I can fix inaccuracies",
        "acceptance_criteria": [
          "Admin code editor: problem statement, Monaco editor for sample code, test case CRUD table",
          "Run button executes sample code and streams output back",
          "'Save Draft' persists without publishing",
          "'Publish' adds to question bank",
          "'Regenerate' saves current as draft and re-triggers AI with same params"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A2-03",
          "title": "Admin runs sample code and receives streamed output",
          "steps": [
            "Open AI-generated question in admin editor",
            "Edit sample code if needed",
            "Click Run"
          ],
          "expected_result": "Code executed; output streamed back"
        },
        {
          "id": "TS-A2-04",
          "title": "Admin saves question as draft without publishing",
          "steps": [
            "Open AI-generated question",
            "Make edits",
            "Click Save Draft"
          ],
          "expected_result": "Question persisted as draft; not in published bank"
        },
        {
          "id": "TS-A2-05",
          "title": "Admin publishes AI-generated question to question bank",
          "steps": [
            "Open AI-generated question",
            "Click Publish"
          ],
          "expected_result": "Question added to published question bank"
        },
        {
          "id": "TS-A2-06",
          "title": "Admin clicks Regenerate; current saved as draft, new generation triggered",
          "steps": [
            "Open AI-generated question",
            "Click Regenerate"
          ],
          "expected_result": "Current version saved as draft; AI generation re-triggered with same params"
        }
      ],
      "edge_cases": [
        {
          "description": "Run does not affect the question bank",
          "expected_behavior": "Only executes and streams output; question bank unchanged"
        }
      ]
    },
    {
      "epic_id": "A-E2",
      "feature": "Admin manually creates questions with test cases (A-2.3)",
      "qa_story": {
        "title": "As an admin, I should be able to manually create questions with test cases so that I can add questions without AI",
        "acceptance_criteria": [
          "Form fields: title, description, difficulty, topics, subTopics, constraints, sampleCode",
          "Test case table: add/edit/delete rows with input, expectedOutput, isHidden toggle",
          "Save as draft or publish immediately"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A2-07",
          "title": "Admin creates question with all fields and test cases then saves as draft",
          "steps": [
            "Open manual question creation form",
            "Fill all fields",
            "Add test cases; toggle isHidden on some",
            "Click Save Draft"
          ],
          "expected_result": "Question saved as draft; not in published bank"
        },
        {
          "id": "TS-A2-08",
          "title": "Admin creates question and publishes immediately",
          "steps": [
            "Open manual question creation form",
            "Fill all fields and add test cases",
            "Click Publish"
          ],
          "expected_result": "Question published and appears in question bank"
        }
      ],
      "edge_cases": [
        {
          "description": "Test case created with isHidden=true",
          "expected_behavior": "Stored with isHidden=true; candidates see only pass/fail for this case"
        }
      ]
    },
    {
      "epic_id": "A-E2",
      "feature": "Admin views, filters, edits, and manages question bank drafts (A-2.4)",
      "qa_story": {
        "title": "As an admin, I should be able to view, filter, edit, and manage drafts for questions in the question bank so that the bank stays organised and accurate",
        "acceptance_criteria": [
          "List: title, difficulty badge, topics, createdAt, usage count, status (DRAFT/PUBLISHED/RETIRED)",
          "Filter by: difficulty, topic, status",
          "Edit creates new version; previous version archived not deleted",
          "Delete is soft-delete (RETIRED); blocked if question in active assessment",
          "Admin can view and promote drafts to published"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A2-09",
          "title": "Admin filters question bank by difficulty, topic, status",
          "steps": [
            "Apply filters: difficulty, topic, status"
          ],
          "expected_result": "List shows only matching questions"
        },
        {
          "id": "TS-A2-10",
          "title": "Editing a question creates new version; previous archived",
          "steps": [
            "Open PUBLISHED question for editing",
            "Make changes and save"
          ],
          "expected_result": "New version created; previous version archived"
        },
        {
          "id": "TS-A2-11",
          "title": "Soft-delete blocked when question in active assessment",
          "steps": [
            "Locate question in active assessment",
            "Attempt to delete"
          ],
          "expected_result": "Delete blocked; question in use"
        },
        {
          "id": "TS-A2-12",
          "title": "Admin promotes draft to published",
          "steps": [
            "Filter by status=DRAFT",
            "Select draft",
            "Promote to published"
          ],
          "expected_result": "Status changes to PUBLISHED; appears in bank"
        }
      ],
      "edge_cases": [
        {
          "description": "Question with usage count > 0 in active assessment",
          "expected_behavior": "Soft-delete blocked; cannot be RETIRED while in use"
        }
      ]
    },
    {
      "epic_id": "A-E4",
      "feature": "Assessment invite email delivery to candidate (A-4.1)",
      "qa_story": {
        "title": "As a candidate, I should be able to receive an assessment invite email with a secure link, instructions, and expiry information so that I know when and how to start my assessment",
        "acceptance_criteria": [
          "Email: assessment name, duration, unique link, expiry timestamp, instructions",
          "Link format: /assess?token={HMAC-signed: userId + assessmentId + expiry}",
          "Dispatched via @Async Spring executor and SendGrid SMTP relay",
          "Link expiry is configurable"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A4-01",
          "title": "Candidate receives invite email with all required content and HMAC-signed link",
          "steps": [
            "Admin triggers invite for a candidate",
            "Candidate opens received email"
          ],
          "expected_result": "Email contains assessment name, duration, HMAC-signed link, expiry timestamp, instructions"
        },
        {
          "id": "TS-A4-02",
          "title": "Invite link contains HMAC-signed token with userId, assessmentId, expiry",
          "steps": [
            "Inspect the link in received invite email"
          ],
          "expected_result": "Link follows /assess?token={HMAC-signed: userId + assessmentId + expiry}"
        }
      ],
      "edge_cases": [
        {
          "description": "Configurable link expiry set to different values",
          "expected_behavior": "Expiry timestamp in email reflects configured duration"
        }
      ]
    },
    {
      "epic_id": "A-E4",
      "feature": "Failed email delivery retry and admin notification (A-4.2)",
      "qa_story": {
        "title": "As the platform, I should be able to retry failed email deliveries and surface them to admins so that no candidate misses their invite silently",
        "acceptance_criteria": [
          "Failed sends retried up to 3 times with exponential backoff: 1s, 4s, 16s",
          "Permanently failed sends flagged in admin invite status list",
          "Admin can trigger manual resend from failed list"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A4-03",
          "title": "Failed email retried 3 times with 1s, 4s, 16s exponential backoff",
          "steps": [
            "Trigger invite in failing state",
            "Observe retry behaviour"
          ],
          "expected_result": "System retries 3 times with delays of 1s, 4s, 16s"
        },
        {
          "id": "TS-A4-04",
          "title": "Permanently failed send flagged in admin list and manually resendable",
          "steps": [
            "Allow all 3 retries to fail",
            "Navigate to admin invite status list",
            "Locate permanently failed send",
            "Trigger manual resend"
          ],
          "expected_result": "Permanently failed flagged; admin can trigger manual resend"
        }
      ],
      "edge_cases": [
        {
          "description": "Retry delay sequence: 1s, 4s, 16s",
          "expected_behavior": "Each retry follows exact exponential backoff schedule"
        }
      ]
    },
    {
      "epic_id": "A-E5",
      "feature": "Admin per-assessment analytics dashboard (A-5.1)",
      "qa_story": {
        "title": "As an admin, I should be able to view a per-assessment analytics page showing all candidates' results so that I can evaluate the cohort",
        "acceptance_criteria": [
          "Table: name, email, totalScore, attemptsUsed, result, rank",
          "Sortable by score, attempts, time taken; exportable as CSV",
          "Click candidate row to see submitted code and test case breakdown",
          "Score distribution histogram displayed",
          "Data from Team B GET /results/assessment/{id} API"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A5-01",
          "title": "Admin opens analytics; table sortable, CSV-exportable, histogram shown",
          "steps": [
            "Navigate to Statistics Management page",
            "Open per-assessment analytics view"
          ],
          "expected_result": "Table shows all required columns; sorting and CSV export available; histogram shown"
        },
        {
          "id": "TS-A5-02",
          "title": "Admin clicks candidate row and sees submitted code and test case breakdown",
          "steps": [
            "Click a candidate row in analytics table"
          ],
          "expected_result": "Drill-down shows submitted code and test case breakdown"
        }
      ],
      "edge_cases": [
        {
          "description": "Table sorted by score descending",
          "expected_behavior": "Candidates ranked highest to lowest"
        }
      ]
    },
    {
      "epic_id": "A-E5",
      "feature": "Admin views user-specific statistics across all assessments (A-5.2)",
      "qa_story": {
        "title": "As an admin, I should be able to view user-specific statistics across all assessments so that I can track individual candidate performance over time",
        "acceptance_criteria": [
          "Statistics cards: total assigned, total attempted, avg score, best score",
          "Assessment history table per user",
          "Accessible from User Management > User Detail page",
          "Data from Team B GET /results/user/{id} API"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-A5-03",
          "title": "Admin navigates to User Detail and sees statistics cards and history table",
          "steps": [
            "Navigate to User Management",
            "Open a user detail page"
          ],
          "expected_result": "Statistics cards: total assigned, attempted, avg score, best score; history table shown"
        }
      ],
      "edge_cases": [
        {
          "description": "User with no completed assessments",
          "expected_behavior": "Statistics cards show zero/empty; history table empty"
        }
      ]
    },
    {
      "epic_id": "INT",
      "feature": "Integration contract: GET /assessments/{id}/config — Team A exposes, Team B consumes at session start",
      "qa_story": {
        "title": "As Team B candidate platform, I should be able to read assessment configuration via GET /assessments/{id}/config at session start so that the candidate session is initialised with the correct parameters",
        "acceptance_criteria": [
          "Returns: assessmentId, questionId, durationMinutes, maxAttempts, passThresholdPct",
          "Owned and exposed by Team A",
          "Team B reads at session start via API — no direct DB join"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-INT-01",
          "title": "GET /assessments/{id}/config returns all required fields",
          "steps": [
            "Team B client calls GET /assessments/{id}/config with valid assessmentId at session start"
          ],
          "expected_result": "Response contains assessmentId, questionId, durationMinutes, maxAttempts, passThresholdPct"
        },
        {
          "id": "TS-INT-02",
          "title": "Invalid assessmentId returns error",
          "steps": [
            "Team B client calls GET /assessments/{id}/config with non-existent assessmentId"
          ],
          "expected_result": "API returns error indicating assessment not found"
        }
      ],
      "edge_cases": [
        {
          "description": "Config requested for DRAFT-status assessment",
          "expected_behavior": "Behaviour per Team A implementation; Team B handles non-ACTIVE states gracefully"
        }
      ]
    },
    {
      "epic_id": "INT",
      "feature": "Integration contract: GET /questions/{id} and GET /assessments/{id}/testcases — Team A exposes, Team B reads",
      "qa_story": {
        "title": "As Team B candidate platform, I should be able to read question details and test cases via GET /questions/{id} and GET /assessments/{id}/testcases at session start so that the code editor is populated correctly",
        "acceptance_criteria": [
          "GET /questions/{id} returns question details for candidate session",
          "GET /assessments/{id}/testcases returns test cases with isVisible and weight fields",
          "Both endpoints owned and exposed by Team A",
          "Team B reads via API — no direct DB join"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-INT-03",
          "title": "GET /questions/{id} returns question details",
          "steps": [
            "Team B client calls GET /questions/{id} with valid questionId at session start"
          ],
          "expected_result": "Response contains question details"
        },
        {
          "id": "TS-INT-04",
          "title": "GET /assessments/{id}/testcases returns test cases with isVisible and weight",
          "steps": [
            "Team B client calls GET /assessments/{id}/testcases with valid assessmentId"
          ],
          "expected_result": "Response contains test cases each with isVisible and weight fields"
        }
      ],
      "edge_cases": [
        {
          "description": "Test case with isVisible=false",
          "expected_behavior": "Returned with isVisible=false; Team B must not expose actual output to candidate"
        }
      ]
    },
    {
      "epic_id": "INT",
      "feature": "Integration contract: GET /results/assessment/{id} and GET /results/user/{id} — Team B exposes, Team A reads",
      "qa_story": {
        "title": "As Team A admin platform, I should be able to read scoring data via GET /results/assessment/{id} and GET /results/user/{id} so that the admin analytics dashboard can query submission data without coupling to Team B internals",
        "acceptance_criteria": [
          "GET /results/assessment/{id} returns paginated candidate results (consumed by A-5.1)",
          "GET /results/user/{id} returns per-user assessment history (consumed by A-5.2)",
          "Both require valid ADMIN role JWT",
          "Both owned and exposed by Team B"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-INT-05",
          "title": "GET /results/assessment/{id} returns paginated results with valid ADMIN JWT",
          "steps": [
            "Call GET /results/assessment/{id} with valid ADMIN JWT"
          ],
          "expected_result": "Paginated candidate results returned"
        },
        {
          "id": "TS-INT-06",
          "title": "GET /results/user/{id} returns per-user history with valid ADMIN JWT",
          "steps": [
            "Call GET /results/user/{id} with valid ADMIN JWT"
          ],
          "expected_result": "Per-user assessment history returned"
        },
        {
          "id": "TS-INT-07",
          "title": "Both results endpoints reject non-ADMIN JWT",
          "steps": [
            "Call both endpoints without JWT or with USER role JWT"
          ],
          "expected_result": "Both return authorisation error"
        }
      ],
      "edge_cases": [
        {
          "description": "Results endpoint called for assessment with no submissions",
          "expected_behavior": "Returns empty paginated result; no error"
        }
      ]
    },
    {
      "epic_id": "INT",
      "feature": "Integration contract: WebSocket RUN/OUTPUT/DONE message contract between Team A server and Team B client",
      "qa_story": {
        "title": "As the platform, I should be able to route WebSocket RUN messages from the candidate client to the execution engine and stream OUTPUT and DONE messages back so that candidates receive real-time code execution results",
        "acceptance_criteria": [
          "Team A owns the WebSocket server handler and session routing map",
          "Team B owns the WebSocket client in the candidate code editor",
          "RUN message: {type: RUN, sessionId, language: java, code}",
          "Server streams OUTPUT: {type: OUTPUT, line}",
          "Server sends DONE on completion",
          "Cross-session routing prevented via JWT sessionId claim validation"
        ]
      },
      "test_scenarios": [
        {
          "id": "TS-INT-08",
          "title": "Candidate sends RUN; receives streamed OUTPUT lines then DONE",
          "steps": [
            "Candidate opens code editor (WS connected with JWT)",
            "Candidate clicks Run",
            "Team B client sends {type: RUN, sessionId, language: java, code}"
          ],
          "expected_result": "Server streams {type: OUTPUT, line} for each line, then sends DONE"
        },
        {
          "id": "TS-INT-09",
          "title": "WS handler rejects cross-session RUN via JWT sessionId claim validation",
          "steps": [
            "Send RUN message with sessionId not matching JWT sessionId claim"
          ],
          "expected_result": "WS handler rejects message; cross-session routing prevented"
        }
      ],
      "edge_cases": [
        {
          "description": "RUN sent while previous execution still in progress for same session",
          "expected_behavior": "Behaviour governed by Team A WS handler implementation"
        }
      ]
    }
  ]
}

output_path = r'c:\Users\UjjwalSharma\Desktop\TestingAgents\outputs\qa_output.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f'Written {len(data["features"])} features to {output_path}')

