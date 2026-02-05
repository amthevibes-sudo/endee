"""Command-line interface for PDF semantic search."""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from config import Config
from search_engine import SemanticSearchEngine

console = Console()


@click.group()
def cli():
    """PDF Semantic Search Engine powered by Endee."""
    pass


@cli.command()
@click.option('--pdf-dir', type=click.Path(exists=True), help='Directory containing PDFs')
def ingest(pdf_dir):
    """Ingest PDFs into the search engine."""
    engine = SemanticSearchEngine()
    
    # Initialize collection
    if not engine.initialize():
        console.print("[red]Failed to initialize Endee collection[/red]")
        return
    
    # Ingest PDFs
    pdf_path = Path(pdf_dir) if pdf_dir else Config.PDF_DIR
    
    if not pdf_path.exists():
        console.print(f"[red]Directory not found: {pdf_path}[/red]")
        return
    
    success = engine.ingest_pdfs(pdf_path)
    
    if success:
        console.print("\n[green]✓ Ingestion completed successfully![/green]")
    else:
        console.print("\n[red]✗ Ingestion failed[/red]")


@cli.command()
@click.argument('query')
@click.option('--top-k', default=5, help='Number of results to return')
@click.option('--file', help='Filter by specific filename')
def search(query, top_k, file):
    """Search for relevant document chunks."""
    engine = SemanticSearchEngine()
    
    console.print(f"\n[bold cyan]Searching for:[/bold cyan] {query}\n")
    
    results = engine.search(query, top_k=top_k, filter_by_file=file)
    
    if not results:
        console.print("[yellow]No results found[/yellow]")
        return
    
    # Display results
    for i, result in enumerate(results, 1):
        metadata = result.get('metadata', {})
        score = result.get('score', 0.0)
        
        # Create result panel
        title = f"Result {i} - {metadata.get('file_name', 'Unknown')} (Page {metadata.get('page', '?')})"
        
        content = f"""
**Score:** {score:.4f}

**Text:**
{metadata.get('text', 'No text available')}

**Source:** {metadata.get('file_path', 'Unknown')}
**Page:** {metadata.get('page', '?')}
**Chunk ID:** {metadata.get('chunk_id', '?')}
"""
        
        panel = Panel(
            Markdown(content),
            title=title,
            border_style="cyan" if i == 1 else "blue"
        )
        
        console.print(panel)
        console.print()


@cli.command()
def info():
    """Display information about the current index."""
    engine = SemanticSearchEngine()
    
    index_info = engine.get_index_info()
    
    if not index_info:
        console.print("[yellow]No index found. Run 'ingest' first.[/yellow]")
        return
    
    # Display index information
    console.print("\n[bold cyan]Index Information[/bold cyan]\n")
    
    console.print(f"[bold]Total Chunks:[/bold] {index_info.get('total_chunks', 0)}")
    console.print(f"[bold]Embedding Model:[/bold] {index_info.get('embedding_model', 'Unknown')}")
    console.print(f"[bold]Embedding Dimension:[/bold] {index_info.get('embedding_dimension', 'Unknown')}")
    
    # Files table
    files = index_info.get('files', {})
    
    if files:
        console.print("\n[bold]Indexed Files:[/bold]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("File Name", style="cyan")
        table.add_column("Chunks", justify="right")
        table.add_column("Pages", justify="right")
        
        for filename, file_data in files.items():
            table.add_row(
                filename,
                str(file_data.get('chunks', 0)),
                str(len(file_data.get('pages', [])))
            )
        
        console.print(table)
    
    console.print()


@cli.command()
@click.confirmation_option(prompt='Are you sure you want to reset the index?')
def reset():
    """Reset the search index (delete all data)."""
    engine = SemanticSearchEngine()
    
    if engine.reset_index():
        console.print("[green]✓ Index reset successfully[/green]")
    else:
        console.print("[red]✗ Failed to reset index[/red]")


@cli.command()
def interactive():
    """Start interactive search mode."""
    engine = SemanticSearchEngine()
    
    console.print("\n[bold cyan]PDF Semantic Search - Interactive Mode[/bold cyan]")
    console.print("Type your query or 'quit' to exit\n")
    
    while True:
        try:
            query = console.input("[bold green]Search:[/bold green] ")
            
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("\n[yellow]Goodbye![/yellow]\n")
                break
            
            if not query.strip():
                continue
            
            console.print()
            results = engine.search(query, top_k=3)
            
            if not results:
                console.print("[yellow]No results found[/yellow]\n")
                continue
            
            for i, result in enumerate(results, 1):
                metadata = result.get('metadata', {})
                score = result.get('score', 0.0)
                
                console.print(f"[bold cyan]{i}. {metadata.get('file_name', 'Unknown')} (Page {metadata.get('page', '?')}) - Score: {score:.4f}[/bold cyan]")
                
                text = metadata.get('text', '')
                preview = text[:200] + "..." if len(text) > 200 else text
                console.print(f"   {preview}\n")
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Goodbye![/yellow]\n")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]\n")


if __name__ == '__main__':
    cli()
