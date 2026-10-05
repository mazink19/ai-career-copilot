from langgraph.graph import END, START, StateGraph

from app.ai.analyzers.job_matcher import JobMatcher

from app.graph.job_matching.state import JobMatchingState
from app.graph.job_matching.nodes import (
    make_analyze_match_node,
    route_match,
    good_match_node,
    weak_match_node,
)

def build_job_matching_graph(
    matcher: JobMatcher,
):

    graph = StateGraph(JobMatchingState)

    analyze_match = make_analyze_match_node(matcher)

    graph.add_node("analyze_match",  analyze_match,)
    graph.add_node("good_match", good_match_node,)
    graph.add_node("weak_match", weak_match_node,)

    graph.add_edge(START,"analyze_match",)
    graph.add_conditional_edges("analyze_match",
        route_match,
        {
            "good_match": "good_match",
            "weak_match": "weak_match",
        },
    )

    graph.add_edge("good_match",END,)
    graph.add_edge("weak_match",END,)

    return graph.compile()