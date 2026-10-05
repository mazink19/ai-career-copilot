from langgraph.graph import StateGraph, START, END

from app.graph.state import ResumeAnalysisState
from app.graph.nodes import (
    make_create_analysis_node,
    make_mark_analyzing_node,
    make_extract_resume_node,
    make_analyze_resume_node,
    make_save_analysis_node,
    route_after_analysis,
    make_handle_failure_node
)


def build_resume_analysis_graph(extractor,analyzer,analysis_repository,):

    graph = StateGraph(ResumeAnalysisState)

    create_node = make_create_analysis_node(analysis_repository)
    analyzing_node = make_mark_analyzing_node(analysis_repository)
    extract_node = make_extract_resume_node(extractor)
    analyze_node = make_analyze_resume_node(analyzer)
    save_node = make_save_analysis_node(analysis_repository)
    failure_node = make_handle_failure_node(analysis_repository)


    graph.add_node("create_analysis", create_node)
    graph.add_node("mark_analyzing", analyzing_node)
    graph.add_node("extract_resume", extract_node)
    graph.add_node("analyze_resume", analyze_node)
    graph.add_node("save_analysis", save_node)
    graph.add_node("handle_failure", failure_node)

    graph.add_edge(START, "create_analysis")
    graph.add_edge("create_analysis", "mark_analyzing")
    graph.add_edge("mark_analyzing", "extract_resume")
    graph.add_edge("extract_resume", "analyze_resume")

    graph.add_conditional_edges(
    "analyze_resume",
    route_after_analysis,
    {
        "success": "save_analysis",
        "failure": "handle_failure",
    },
)
    graph.add_edge("save_analysis", END)
    graph.add_edge("handle_failure", END)

    return graph.compile()