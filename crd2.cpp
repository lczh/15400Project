
#include <bits/stdc++.h>
using namespace std;
#define FOR(index, start, end) for(int index = start; index < end; ++index)
#define F0R(index, end) for(int index = 0; index < end; ++index)
#define RFOR(index, start, end) for(int index = start; index > end; --index)
#define FOREACH(itr, b) for(auto itr = b.begin(); itr != b.end(); ++itr)
#define RFOREACH(itr, b)  qfor(auto itr = b.rbegin(); itr != b.rend(); ++itr)
#define db(x) cerr << #x << " = " << x << endl
#define db2(x, y) cerr << #x << " = " << x << ", " << #y << " = " << y << endl
#define db3(x, y, z) cerr << #x << " = " << x << ", " << #y << " = " << y << ", " << #z << " = " << z << endl
#define ri(x) scanf("%d", &x)
#define ri2(x, y) scanf("%d%d", &x, &y)
#define ri3(x, y, z) scanf("%d%d%d", &x, &y, &z)
#define rll(x) scanf("%lld", &x)
#define INF 1000000000
#define M 1000000007
#define MAXN 15625005
typedef long long ll;
typedef long double ld;
typedef pair<int, int> pii;

// this version chooses the most recently added active node.

vector<pii> edges[MAXN];
int l[MAXN];
int m[MAXN];
deque<int> D;
bool inD[MAXN];
int h;
int n;


struct compare{
    bool operator() (int u, int v) const{
        if (l[u] != l[v]){
            return l[u] < l[v];
        }
        return u < v;
    }
};

//returns the degree of u
int d(int u){
    return edges[u].size();
}

// returns the excess mass on u
int ex(int u){
    return max(0, m[u] - d(u));
}

//returns the total mass in the graph
int totalmass(){
    int ans = 0;
    for(int i = 0; i < n; i++){
        ans += m[i];
    }
    return ans;
}


void relabel(int u){
    l[u]++;
    inD[D.back()] = false;
    D.pop_back();
    if (l[u] != h){
        inD[u] = true;
        D.push_front(u);
    }
}


void push(int u, int i){
    pii edge = edges[u][i];
    int r = l[u] - edge.second;
    int v = edge.first;
    int x = min(ex(u), min(r, 2 * d(v) - m[v]));
    edges[u][i].second += x;
    for(int i = 0; i < edges[v].size(); i++){
        if (edges[v][i].first == u){
            edges[v][i].second -= x;
        }
    }
    m[u] -= x;
    m[v] += x;
    if (m[u] <= d(u)){
        inD[D.back()] = false;
        D.pop_back();
    }
    if (m[v] > d(v) && !inD[v]){ // fix this, dont add it twice!
        inD[v] = true;
        D.push_back(v);
    }
}
void pushrelabel(int u){
    for(int i = 0; i < edges[u].size(); i++){
        int v = edges[u][i].first;
        if (l[u] > l[v] && edges[u][i].second < l[u] && m[v] < 2 * d(v)){
            push(u, i);
            return;
        }
    }
    relabel(u);
}

vector<int> levelCut(int level){
    vector<int> C;
    for(int i = 0; i < n; i++){
        if (l[i] >= level){
            C.push_back(i);
        }
    }
    return C;
}

bool inC[MAXN];
int cross;
ld conductance(vector<int> C){
    fill(inC, inC + n, false);
    for(int u : C){
        inC[u] = true;
    }
    int vol1 = 0;
    int vol2 = 0;
    cross = 0;
    for(int u = 0; u < n; u++){
        for(pii p : edges[u]){
            int v = p.first;
            if (inC[u] && !inC[v]){
                cross++;
            }
        }
    }
    for(int u = 0; u < n; u++){
        if (inC[u]){
            vol1 += d(u);
        }
        else{
            vol2 += d(u);
        }
    }
    if (vol1 == 0 || vol2 == 0) {
		return INF;
	}
    return (ld)cross / min(vol1, vol2);
}

void add(int u){
    for(pii p : edges[u]){
        int v = p.first;
        if (inC[v]){
            cross--;
        }
        else{
            cross++;
        }
    }
    inC[u] = true;
}


vector<int> getBestCut(int source){
    fill(inC, inC + n, false);
    vector<int> v;
    FOR(i, 0, n){
        v.push_back(i);
    }
    sort(v.begin(), v.end(), compare());
    int besti = -1;
    bool containsSource = false;
    ld bestCond = 2 * INF;
    cross = 0;
    int sourcei = -1;
    RFOR(i, n - 1, -1){
        int level = l[v[i]];
        while(i >= 0 && l[v[i]] == level){
            add(v[i]);
            if (v[i] == source){
                containsSource = true;
                sourcei = i;
            }
            i--;
        }
        i++;
        ld cond = ( min(n - i, i) == 0 ? INF : (ld)cross / min(n - i, i));
        if (containsSource && cond < bestCond){
            bestCond = cond;
            besti = i;
        }
    }
    vector<int> C;
    FOR(i, besti, n){
        C.push_back(v[i]);
    }
    return C;
}
vector<int> getCut(int source){
    return levelCut(l[source]);
}

void inner_flow(int source, ld phi){
    // initialize
    for(int i = 0; i < n; i++){
        l[i] = 0;
        for(int j = 0; j < edges[i].size(); j++){
            edges[i][j].second = 0;
        }
    }

    vector<int> v;
    D = deque<int>();
    for(int i = 0; i < n; i++){
        if (m[i] > d(i)){
            v.push_back(i);
        }
    }
    random_shuffle(v.begin(), v.end());
    for(int u : v){
        inD[u] = true;
        D.push_back(u);
    }

    h = 3 * log2(totalmass()) / phi;
    db(h);
    //flow
    while(!D.empty()){
        int u = D.back();
        pushrelabel(u);
    }
}

int iterations = 0;

vector<int> crd(int source, ld phi, ld r, int t){
    //initialization
    fill(m, m + n, 0);

    m[source] = d(source);
    int maxmass = d(source);


    vector<int> ans;
    for(int j = 0; j <= t; j++){
        for(int i = 0; i < n; i++){
            m[i] *= 2;
        }
        maxmass *= 2;
        inner_flow(source, phi);
        iterations++;
        for(int i = 0; i < n; i++){
            m[i] = min(m[i], d(i));
        }
        if (totalmass() <= r * maxmass){
            break;
        }
    }
    for(int i = 0; i < n; i++){
        m[i] *= 2;
    }
    maxmass *= 2;
    inner_flow(source, phi);
    return getBestCut(source);
}

void addEdge(int u, int v){
    edges[u].push_back({v, 0});
    edges[v].push_back({u, 0});
}

void gen1(){ // tree cross line
    n = 1000000;
    int n1 = 10000;
    int n2 = 100;

    FOR(i, 0, n){
        edges[i].clear();
    }

    FOR(tree, 0, n2){
        FOR(i, 0, n1){
            FOR(j, 2 * i + 1, 2 * i + 3){
                if (j < n1){
                    addEdge(tree * n1 + i, tree * n1 + j);
                }
            }
        }
    }
    FOR(i, 0, n){
        int j = i + n1;
        if (j < n){
            addEdge(i, j);
        }
    }
    FOR(i, 0, n){
        random_shuffle(edges[i].begin(), edges[i].end());
    }
}

void gen2(){ // grid
    n = 1000000;
    int side = 1000;

    FOR(i, 0, n){
        edges[i].clear();
    }

    FOR(i, 0, side){
        FOR(j, 0, side){
            int u = i * side + j;
            if (j < side - 1){
                addEdge(u, u + 1);
            }
            if (i < side - 1){
                addEdge(u, u + side);
            }
        }
    }
    FOR(i, 0, n){
        random_shuffle(edges[i].begin(), edges[i].end());
    }
}
void gen3(){ // two stars cross line
    n = 1000000;
    int n1 = 10000;
    int n2 = 100;

    FOR(i, 0, n){
        edges[i].clear();
    }

    FOR(tree, 0, n2){
        FOR(i, 2, n1){
            addEdge(tree * n1 + i, tree * n1 + i % 2);
        }
        addEdge(tree * n1 + 3, tree * n1 + 4);
    }
    FOR(i, 0, n){
        int j = i + n1;
        if (j < n){
            addEdge(i, j);
        }
    }
    FOR(i, 0, n){
        random_shuffle(edges[i].begin(), edges[i].end());
    }
}
int cnt1 = 0;
int cnt2 = 0;
void printVector(vector<int> v){
    cout << v.size() << endl;
    for(int x : v){
        cout << x << " ";
    }
    cout << endl;
}

int main(){
    srand(420);
    freopen("out.txt", "w", stdout);
    gen1();
    vector<int> v = crd(1, 0.1, 0.9, 18);


    sort(v.begin(), v.end());
    printVector(v);

    db(iterations);
    db2(cnt1, cnt2);
}
