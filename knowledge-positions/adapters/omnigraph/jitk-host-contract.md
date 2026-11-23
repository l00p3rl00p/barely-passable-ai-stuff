# OmniGraph automatic JITK host integration (non-normative profile)

These prompt-triggered behavior rules apply only when an OmniGraph agent host opts into this integration; they are not required of every UKC/1 SDK implementation.

When a host implements prompt-triggered JITK:

- Prompts under **15 trimmed characters** bypass automatic discovery.
- Otherwise, identify the likely subject and retrieve a bounded knowledge packet using whichever recorded position, relation and/or proximity methods are available in OmniGraph; use one method or combine them as useful.
- Return **up to five relevant results**, with identities, provenance, positions and immediate associations. Return fewer or none when appropriate.
- Preserve the original human prompt unchanged; supply the bounded knowledge packet separately before intelligence begins work.
- Do not require the consuming LLM to initiate the lookup.

With a relevant packet, even a fresh session starts at gate 1 with useful knowledge. Do not repeat the host's discovery. An empty or bypassed packet does not establish that knowledge does not exist; use the gates when the task warrants it.

This is the host integration contract, not an assertion that a prompt hook is installed. OmniGraph and the Knowledge Positions skill work without automatic JITK. Do not simulate an automatic lookup or claim it ran when no host packet exists.

