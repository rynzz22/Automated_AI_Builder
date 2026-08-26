Automated Gemini Orchestrator

A lightweight, multi-agent automation script built with the Google GenAI SDK. It establishes an iterative collaboration loop between two specialized Gemini roles to plan, implement, review, and refine software projects with minimal manual intervention.

Overview

The orchestrator separates software development into two independent agent roles:

Prompter / Architect
Receives a high-level application requirement.
Decomposes the requirement into technical tasks.
Identifies edge cases and implementation constraints.
Produces structured development instructions for the engineering agent.
Developer / Engineer
Consumes the architect's technical specification.
Implements the requested application.
Generates production-oriented source code.
Writes the resulting implementation to a local file.

The system then uses an iterative feedback loop in which the Architect reviews the Engineer's implementation, identifies defects or improvement opportunities, and provides additional guidance before the final implementation is produced.

Architecture
                    High-Level Application Goal
                               |
                               v
                    +----------------------+
                    | Prompter / Architect |
                    +----------------------+
                               |
                               | Technical Specification
                               v
                    +----------------------+
                    | Developer / Engineer |
                    +----------------------+
                               |
                               | Implementation
                               v
                         Local Codebase
                               |
                               v
                    +----------------------+
                    | Architect Review     |
                    +----------------------+
                               |
                    Feedback / Corrections
                               |
                               v
                    +----------------------+
                    | Developer Revision   |
                    +----------------------+
                               |
                               v
                         Final Output
Requirements
Python 3.10 or later
Google AI Studio API key
Internet connection
google-genai Python package
Installation

Install the required dependency:

pip install google-genai

Configure your Google AI Studio API key through an environment variable or another secure configuration mechanism.

Do not hard-code API keys directly into source code or commit them to a Git repository.

Quick Start

Define the application requirement in the orchestrator:

my_app_idea = "A sleek HTML/CSS/JS digital clock with an integrated countdown stopwatch"

Then execute the orchestration pipeline:

python orchestrator.py

The orchestrator will:

Receive the application requirement.
Generate an architectural specification.
Pass the specification to the Developer agent.
Generate the initial implementation.
Review the implementation.
Produce refinement instructions.
Apply the feedback through another development iteration.
Save the resulting project locally.
Iterative Development Model

The core workflow can be represented as:

PLAN
  |
  v
IMPLEMENT
  |
  v
REVIEW
  |
  v
REFINE
  |
  +-------> REVIEW
  |
  v
FINALIZE

This approach allows the Architect and Developer to operate as separate responsibilities rather than relying on a single prompt to perform planning, implementation, and quality assurance simultaneously.

Example Application Goal
my_app_idea = """
Build a responsive digital clock using HTML, CSS, and JavaScript.
Include:
- Current time
- Countdown timer
- Stopwatch
- Responsive layout
- Accessible controls
- Clean visual design
"""

The Architect converts this high-level requirement into implementation constraints, while the Developer translates those constraints into the actual source code.

Security Considerations

For production or shared environments:

Store API keys in environment variables or a secrets manager.
Never commit .env files containing credentials.
Add secrets and generated artifacts to .gitignore where appropriate.
Validate generated code before execution.
Do not automatically execute AI-generated commands without sandboxing.
Restrict filesystem access to the intended project directory.
Add timeouts and error handling around API calls.
Implement iteration limits to prevent uncontrolled agent loops.
Limitations

Although the orchestrator can automate substantial portions of development, generated code should still undergo human review.

AI-generated implementations may contain:

Logic errors
Security vulnerabilities
Incorrect assumptions
Dependency issues
Performance problems
Incomplete edge-case handling

The orchestrator should therefore be treated as an automated development assistant, not a replacement for engineering validation, testing, code review, or security assessment.

License

MIT License
