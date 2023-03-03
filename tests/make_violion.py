import plotly.graph_objects as go
from generate_mock_data import get_mock_results
import pandas as pd

parameter = "mass_1"
events = get_mock_results(num_events=3, pts=1000)

event_names = list(events.keys())
posteriors = [e.posterior[parameter] for e in events.values()]
min_samples = min([len(p) for p in posteriors])
posteriors = [p.sample(min_samples) for p in posteriors]
df = pd.DataFrame(dict(zip(event_names, posteriors)))

fig = go.Figure()
fig.add_trace(go.Violin(df, box_visible=True, meanline_visible=True))
fig.show()
