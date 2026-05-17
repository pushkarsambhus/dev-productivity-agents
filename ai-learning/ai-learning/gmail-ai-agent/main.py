#!/usr/bin/env python3
"""Gmail AI Agent — interactive shell and CLI commands powered by Claude."""

import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich import print as rprint

import gmail_client as gmail
import ai_agent as agent

console = Console()


# ─── Helpers ──────────────────────────────────────────────────────────────────

def print_email_table(emails: list[dict], title: str = "Inbox") -> None:
    table = Table(title=title, show_lines=True, highlight=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("ID", style="dim", width=16)
    table.add_column("From", style="cyan", min_width=20)
    table.add_column("Subject", style="bold", min_width=25)
    table.add_column("Date", style="dim", min_width=12)
    table.add_column("", width=2)

    for i, e in enumerate(emails, 1):
        unread = "[green]●[/]" if e.get("unread") else ""
        from_short = e["from"].split("<")[0].strip() or e["from"]
        table.add_row(str(i), e["id"][:16], from_short, e["subject"], e["date"][:16], unread)

    console.print(table)


def pick_email(emails: list[dict]) -> dict | None:
    """Let user pick an email by number or ID from a previously listed set."""
    raw = Prompt.ask("Enter email [bold]#[/] or [bold]ID[/]")
    try:
        idx = int(raw) - 1
        if 0 <= idx < len(emails):
            return emails[idx]
    except ValueError:
        match = next((e for e in emails if e["id"].startswith(raw)), None)
        if match:
            return match
    console.print("[red]Not found.[/]")
    return None


def confirm_and_send(to: str, subject: str, body: str, reply_to: dict | None = None) -> None:
    console.print(Panel(
        f"[bold]To:[/] {to}\n[bold]Subject:[/] {subject}\n\n{body}",
        title="Draft Preview", border_style="yellow"
    ))
    action = Prompt.ask(
        "Send this email?",
        choices=["send", "edit", "cancel"],
        default="send"
    )
    if action == "cancel":
        console.print("[dim]Cancelled.[/]")
        return
    if action == "edit":
        body = click.edit(body) or body

    if Confirm.ask("[bold yellow]Confirm send?[/]", default=False):
        gmail.send_message(to, subject, body, reply_to=reply_to)
        console.print("[green]✓ Sent.[/]")
    else:
        console.print("[dim]Cancelled.[/]")


# ─── Core actions ──────────────────────────────────────────────────────────────

def do_list(query: str, max_results: int) -> list[dict]:
    with console.status("Fetching emails…"):
        emails = gmail.list_messages(query=query, max_results=max_results)
    if not emails:
        console.print("[dim]No emails found.[/]")
        return []
    print_email_table(emails)
    return emails


def do_read(email: dict) -> dict:
    with console.status("Loading email…"):
        full = gmail.get_message(email["id"])
    console.print(Panel(
        f"[bold]From:[/] {full['from']}\n"
        f"[bold]To:[/] {full['to']}\n"
        f"[bold]Date:[/] {full['date']}\n"
        f"[bold]Subject:[/] {full['subject']}\n\n"
        f"{full['body']}",
        title="Email", border_style="blue"
    ))
    suggestion = Prompt.ask(
        "Get AI action suggestion?", choices=["y", "n"], default="n"
    )
    if suggestion == "y":
        with console.status("Thinking…"):
            tip = agent.suggest_action(full)
        console.print(Panel(tip, title="AI Suggestion", border_style="dim"))
    return full


def do_reply(email: dict) -> None:
    with console.status("Loading thread…"):
        full = gmail.get_message(email["id"])
        thread = gmail.get_thread(full["thread_id"])

    instruction = Prompt.ask(
        "Any instructions for Claude? (leave blank for auto)", default=""
    )
    with console.status("Drafting reply…"):
        body = agent.draft_reply(full, thread, instruction)

    # Parse reply-to address
    raw_from = full["from"]
    to = raw_from.split("<")[-1].rstrip(">") if "<" in raw_from else raw_from
    subject = full["subject"]
    if not subject.lower().startswith("re:"):
        subject = "Re: " + subject

    confirm_and_send(to, subject, body, reply_to=full)


def do_compose() -> None:
    to = Prompt.ask("To")
    intent = Prompt.ask("What do you want to say? (describe it)")
    context = Prompt.ask("Any additional context? (optional)", default="")
    with console.status("Composing…"):
        subject, body = agent.compose_email(to, intent, context)
    confirm_and_send(to, subject, body)


def do_summarize(emails: list[dict]) -> None:
    if not emails:
        console.print("[dim]No emails to summarize.[/]")
        return
    with console.status("Summarizing inbox…"):
        summary = agent.summarize_inbox(emails)
    console.print(Panel(summary, title="Inbox Summary", border_style="green"))


def do_summarize_one(email: dict) -> None:
    with console.status("Loading and summarizing…"):
        full = gmail.get_message(email["id"])
        summary = agent.summarize_email(full)
    console.print(Panel(summary, title="Email Summary", border_style="green"))


def do_archive(email: dict) -> None:
    if Confirm.ask(f"Archive '[bold]{email['subject']}[/]'?"):
        gmail.archive_message(email["id"])
        console.print("[green]✓ Archived.[/]")


def do_trash(email: dict) -> None:
    if Confirm.ask(f"[red]Move to trash[/] '[bold]{email['subject']}[/]'?"):
        gmail.trash_message(email["id"])
        console.print("[green]✓ Moved to trash.[/]")


def do_mark(email: dict, read: bool) -> None:
    if read:
        gmail.mark_read(email["id"])
        console.print("[green]✓ Marked as read.[/]")
    else:
        gmail.mark_unread(email["id"])
        console.print("[green]✓ Marked as unread.[/]")


# ─── Interactive shell ─────────────────────────────────────────────────────────

HELP_TEXT = """
[bold]Commands:[/]
  [cyan]list[/] [query]        — List inbox (optional Gmail search query)
  [cyan]search[/] <query>      — Search emails
  [cyan]read[/] <#|id>         — Read an email
  [cyan]reply[/] <#|id>        — AI-draft a reply
  [cyan]compose[/]             — AI-compose a new email
  [cyan]summarize[/]           — Summarize the listed emails
  [cyan]summarize[/] <#|id>    — Summarize a specific email
  [cyan]archive[/] <#|id>      — Archive an email
  [cyan]trash[/] <#|id>        — Move to trash
  [cyan]read-mark[/] <#|id>    — Mark as read
  [cyan]unread-mark[/] <#|id>  — Mark as unread
  [cyan]help[/]                — Show this help
  [cyan]exit[/] / [cyan]quit[/]          — Exit
"""


def run_shell() -> None:
    profile = gmail.get_profile()
    console.print(Panel(
        f"[bold green]Gmail AI Agent[/] — connected as [cyan]{profile.get('emailAddress')}[/]\n"
        "Type [bold]help[/] for commands.",
        border_style="green"
    ))

    emails: list[dict] = []

    while True:
        try:
            raw = Prompt.ask("\n[bold blue]gmail-ai[/]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Bye.[/]")
            break

        if not raw:
            continue

        parts = raw.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ("exit", "quit"):
            console.print("[dim]Bye.[/]")
            break

        elif cmd == "help":
            console.print(HELP_TEXT)

        elif cmd == "list":
            query = arg or "in:inbox"
            emails = do_list(query, max_results=20)

        elif cmd == "search":
            if not arg:
                console.print("[red]Usage: search <query>[/]")
            else:
                emails = do_list(arg, max_results=20)

        elif cmd == "read":
            target = _resolve(arg, emails)
            if target:
                do_read(target)

        elif cmd == "reply":
            target = _resolve(arg, emails)
            if target:
                do_reply(target)

        elif cmd == "compose":
            do_compose()

        elif cmd == "summarize":
            if arg:
                target = _resolve(arg, emails)
                if target:
                    do_summarize_one(target)
            else:
                do_summarize(emails)

        elif cmd == "archive":
            target = _resolve(arg, emails)
            if target:
                do_archive(target)
                emails = [e for e in emails if e["id"] != target["id"]]

        elif cmd == "trash":
            target = _resolve(arg, emails)
            if target:
                do_trash(target)
                emails = [e for e in emails if e["id"] != target["id"]]

        elif cmd == "read-mark":
            target = _resolve(arg, emails)
            if target:
                do_mark(target, read=True)

        elif cmd == "unread-mark":
            target = _resolve(arg, emails)
            if target:
                do_mark(target, read=False)

        else:
            console.print(f"[red]Unknown command:[/] {cmd}. Type [bold]help[/].")


def _resolve(arg: str, emails: list[dict]) -> dict | None:
    """Resolve a number or ID arg to an email dict. Prompts if arg is empty."""
    if not arg:
        if not emails:
            console.print("[red]No emails listed yet. Run 'list' first.[/]")
            return None
        return pick_email(emails)
    try:
        idx = int(arg) - 1
        if 0 <= idx < len(emails):
            return emails[idx]
        console.print("[red]Number out of range.[/]")
        return None
    except ValueError:
        match = next((e for e in emails if e["id"].startswith(arg)), None)
        if match:
            return match
        # Treat as a raw ID and fetch directly
        try:
            with console.status("Fetching…"):
                full = gmail.get_message(arg)
            return full
        except Exception:
            console.print(f"[red]Could not find email: {arg}[/]")
            return None


# ─── Click CLI commands ────────────────────────────────────────────────────────

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Gmail AI Agent — manage your inbox with Claude.\n\nRun without subcommands for interactive shell."""
    if ctx.invoked_subcommand is None:
        run_shell()


@cli.command()
@click.argument("query", default="in:inbox")
@click.option("-n", "--max", default=20, show_default=True, help="Number of emails to fetch")
def list(query, max):
    """List emails matching QUERY (default: inbox)."""
    do_list(query, max)


@cli.command()
@click.argument("query")
@click.option("-n", "--max", default=20, show_default=True)
def search(query, max):
    """Search emails."""
    do_list(query, max)


@cli.command()
@click.argument("msg_id")
def read(msg_id):
    """Read a specific email by ID."""
    with console.status("Loading…"):
        email = gmail.get_message(msg_id)
    do_read(email)


@cli.command()
@click.argument("msg_id")
def reply(msg_id):
    """AI-draft a reply to an email by ID."""
    with console.status("Loading…"):
        email = gmail.get_message(msg_id)
    do_reply(email)


@cli.command()
def compose():
    """AI-compose a new email."""
    do_compose()


@cli.command()
@click.argument("msg_id", required=False)
def summarize(msg_id):
    """Summarize an email (by ID) or the current inbox."""
    if msg_id:
        with console.status("Loading…"):
            email = gmail.get_message(msg_id)
        do_summarize_one(email)
    else:
        with console.status("Fetching inbox…"):
            emails = gmail.list_messages()
        do_summarize(emails)


@cli.command()
@click.argument("msg_id")
def archive(msg_id):
    """Archive an email by ID."""
    with console.status("Loading…"):
        email = gmail.get_message(msg_id)
    do_archive(email)


@cli.command()
@click.argument("msg_id")
def trash(msg_id):
    """Move an email to trash by ID."""
    with console.status("Loading…"):
        email = gmail.get_message(msg_id)
    do_trash(email)


if __name__ == "__main__":
    cli()
