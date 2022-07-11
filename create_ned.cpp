#include <iostream>
#include <string>
#include <jsoncpp/json/json.h>
#include <fstream>
#include <vector>
#include <sstream>

using namespace std;
using namespace Json;

string filename;
vector<int> node_degree;
vector<vector<int>> link;

void create_head(ofstream &ofs)
{
    ofs << "package inet.examples.bgpv4.BgpUpdate;\n\n";
    ofs << "import inet.common.misc.ThruputMeteringChannel;\n";
    ofs << "import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;\n";
    ofs << "import inet.node.bgp.BgpRouter;\n";
    ofs << "import inet.node.ethernet.EtherSwitch;\n";
    ofs << "import inet.node.inet.StandardHost;\n";
    ofs << "import inet.node.ospfv2.OspfRouter;\n";
    ofs << "import inet.visualizer.integrated.IntegratedCanvasVisualizer;\n" << endl;
    return ;
}

string Link = "LINK_100";
string delay = "50us";
string datarate = "100Mbps";
string displayAsTooltip = "true";
string thruputDisplayFormat = "\"#N\"";

void create_types(ofstream &ofs)
{

    ofs << "\ttypes:\n"; 
    ofs << "\t\tchannel " << Link << " extends ThruputMeteringChannel\n";
    ofs << "\t\t{\n";
    ofs << "\t\t\tparameters:\n";
    ofs << "\t\t\t\tdelay = " << delay << ";\n";
    ofs << "\t\t\t\tdatarate = " << datarate << ";\n";
    ofs << "\t\t\t\tdisplayAsTooltip = " << displayAsTooltip << ";\n";
    ofs << "\t\t\t\tthruputDisplayFormat = " << thruputDisplayFormat << ";\n";
    ofs << "\t\t}" << endl;
    
}

void get_node_degree()
{
    Reader reader;
    Value value;
    ifstream ifs; 
    ifs.open(filename, ios::binary);
    reader.parse(ifs, value);
    const Value arrayNode = value["nodes"];
    const int nodeSize = arrayNode.size();
    //cout << nodeSize << endl;
    for (int i = 0; i < nodeSize; ++i) 
    {
        int x = arrayNode[i]["degree"].asInt();
        node_degree.push_back(x);
    }
    return ;
}

void get_link()
{
    Reader reader;
    Value value;
    ifstream ifs; 
    ifs.open(filename, ios::binary);
    reader.parse(ifs, value);
    const Value arrayLink = value["links"];
    const int linkSize = arrayLink.size();
    for (int i = 0; i < linkSize; ++i)
    {
        int x = arrayLink[i]["source"].asInt();
        int y = arrayLink[i]["target"].asInt();
        int z = arrayLink[i]["betweenness"].asInt(); //
        // link.push_back({x, y});
        link.push_back({x, y, z});
    }   
    return ;
}

string create_bgp_position() 
{
    int x = 300, y = 300;
    const int line = 15;
    static int cnt = 0;
    ++cnt;
    x += (cnt % 15) * 150;
    y += (cnt / 15) * 150;
    ostringstream format;
    format << "\t\t\t\t@display(\"p=" << x << "," << y << "\");";
    return format.str();
}

string create_host_position() 
{
    int x = 350, y = 300;
    const int line = 15;
    static int cnt = 0;
    ++cnt;
    x += (cnt % 15) * 150;
    y += (cnt / 15) * 150;
    ostringstream format;
    format << "\t\t\t\t@display(\"p=" << x << "," << y << ";i=device/pc\");";
    return format.str();
}

string create_swich_position() 
{
    int x = 350, y = 350;
    const int line = 15;
    static int cnt = 0;
    ++cnt;
    x += (cnt % 15) * 150;
    y += (cnt / 15) * 150;
    ostringstream format;
    format << "\t\t\t\t@display(\"p=" << x << "," << y << "\");";
    return format.str();
}

void create_node(ofstream &ofs, string s) 
{
    for (int i = 0; i < node_degree.size(); ++i)
    {
        ostringstream format;
        format << s << i;
        string S = format.str();
        if (s == string("A")) {
            ofs << "\t\t" << S << ": BgpRouter {\n";
            ofs << "\t\t\tparameters:\n";
            ofs << create_bgp_position() << "\n";
        } else if (s == string("HA")) {
            ofs << "\t\t" << S << ": StandardHost {\n";
            ofs << "\t\t\tparameters:\n";
            ofs << create_host_position() << "\n";
        } else if (s == string("PA")) {
            ofs << "\t\t" << S << ": EtherSwitch {\n";
            ofs << "\t\t\tparameters:\n";
            ofs << create_swich_position() << "\n";
        }
        ofs << "\t\t\tgates:\n";
        if (s == string("A")) {
            ofs << "\t\t\t\t" << "pppg[" << node_degree[i]  << "];\n";
            ofs << "\t\t\t\t" << "ethg[1];\n";
            ofs << "\t\t}\n";
        } else if (s == string("HA")) {
            ofs << "\t\t\t\t" << "ethg[1];\n";
            ofs << "\t\t}\n";
        } else if (s == string("PA")) {
            ofs << "\t\t\t\t" << "ethg[2];\n";
            ofs << "\t\t}\n";
        }
    }
    return ;
}

void create_submodules(ofstream &ofs) 
{
    ofs << "\tsubmodules:\n";

    // @display(\"p=100,100;is=s\"); 怎么设置
    ofs << "\t\tvisualizer: IntegratedCanvasVisualizer {\n";
    ofs << "\t\t\tparameters:\n";
    ofs << "\t\t\t\t@display(\"p=100,100;is=s\");\n";
    ofs << "\t\t}\n";

    ofs << "\t\tconfigurator: Ipv4NetworkConfigurator {\n";
    ofs << "\t\t\tparameters:\n";
    ofs << "\t\t\t\t@display(\"p=100,200;is=s\");\n";
    ofs << "\t\t\t\tconfig = xmldoc(\"IPv4Config.xml\");\n";
    ofs << "\t\t\t\taddStaticRoutes = false;\n";
    ofs << "\t\t\t\taddDefaultRoutes = false;\n";
    ofs << "\t\t\t\taddSubnetRoutes = false;\n";
    ofs << "\t\t}\n";
    create_node(ofs, "A");
    create_node(ofs, "HA");
    create_node(ofs, "PA");
    return ;
}

void create_connections(ofstream &ofs)
{
    int A[300] = {0};
    
    ofs << "\tconnections:\n";
    for (int i = 0; i < link.size(); ++i) {
        ostringstream formatA1, formatA2, linkNum;
        formatA1 << "A" << link[i][0];
        formatA2 << "A" << link[i][1];

        //  21/06/24
        if(link[i][2] == 0) {
            linkNum << "LINK_1";
        }
        else {
            linkNum << "LINK_" << link[i][2];
        }
        
        
        ofs << "\t\t" << formatA1.str() << ".pppg[" << A[link[i][0]]++ << "] <--> " <<  linkNum.str() << " <--> "
        << formatA2.str() << ".pppg[" << A[link[i][1]]++ << "];\n";
    }
    
    for (int i = 0; i < node_degree.size(); ++i) {
        ostringstream formatA, formatP, formatH;
        formatA << "A" << i;
        formatP << "PA" << i;
        formatH << "HA" << i;
        ofs << "\t\t" <<  formatP.str() << ".ethg[1] <--> LINK_100 <--> " << formatH.str()
        << ".ethg[0];\n";
        ofs << "\t\t" <<  formatA.str() << ".ethg[0] <--> LINK_100 <--> " << formatP.str()
        << ".ethg[0];\n";
    }
    

/*
    //生成session id
    for (int i = 0; i < link.size(); ++i) {
        ostringstream formatA1, formatA2;
        formatA1 << "A" << link[i][0];
        formatA2 << "A" << link[i][1];
        // ofs << "\t\t" << formatA1.str() << ".pppg[" << A[link[i][0]]++ << "] <--> LINK_100 <--> "
        // << formatA2.str() << ".pppg[" << A[link[i][1]]++ << "]\n";
        if(i < 246) {
            ofs << "  " << "<Session id=\"1\">\n";
            ofs << "    " << "<Router exterAddr=\"10.10." << i+10 << ".1\" > </Router> <!--Router " << formatA1.str() << "-->\n";
            ofs << "    " << "<Router exterAddr=\"10.10." << i+10 << ".2\" > </Router> <!--Router " << formatA2.str() << "-->\n";
            ofs << "  " << "</Session>\n";
        }else {
            ofs << "  " << "<Session id=\"1\">\n";
            ofs << "    " << "<Router exterAddr=\"10.11." << i-236 << ".1\" > </Router> <!--Router " << formatA1.str() << "-->\n";
            ofs << "    " << "<Router exterAddr=\"10.11." << i-236 << ".2\" > </Router> <!--Router " << formatA2.str() << "-->\n";
            ofs << "  " << "</Session>\n";
        }
        
    }


    //生成ipv4 config
    for (int i = 0; i < link.size(); ++i) {
        ostringstream formatA1, formatA2;
        formatA1 << "A" << link[i][0];
        formatA2 << "A" << link[i][1];
        // ofs << "\t\t" << formatA1.str() << ".pppg[" << A[link[i][0]]++ << "] <--> LINK_100 <--> "
        // << formatA2.str() << ".pppg[" << A[link[i][1]]++ << "]\n";
        if(i < 246) {
            ofs << "<interface hosts='" << formatA1.str() << "' names='ppp" << A[link[i][0]]++ << "' address='10.10." 
            << i+10 << ".1' netmask='255.255.255.0' groups='224.0.0.1 224.0.0.2 224.0.0.5' metric='1'/>\n";
            ofs << "<interface hosts='" << formatA2.str() << "' names='ppp" << A[link[i][1]]++ << "' address='10.10." 
            << i+10 << ".2' netmask='255.255.255.0' groups='224.0.0.1 224.0.0.2 224.0.0.5' metric='1'/>\n";
        }else {
            ofs << "<interface hosts='" << formatA1.str() << "' names='ppp" << A[link[i][0]]++ << "' address='10.11." 
            << i-236 << ".1' netmask='255.255.255.0' groups='224.0.0.1 224.0.0.2 224.0.0.5' metric='1'/>\n";
            ofs << "<interface hosts='" << formatA2.str() << "' names='ppp" << A[link[i][1]]++ << "' address='10.11." 
            << i-236 << ".2' netmask='255.255.255.0' groups='224.0.0.1 224.0.0.2 224.0.0.5' metric='1'/>\n";
        }
        
    }
    */

    return ;
}

int main(int argc, char *argv[]) 
{

    ofstream ofs("Network.ned");
    create_head(ofs);
    ofs << "network BgpNetwork\n{\n" << endl;

    // 生成结点和边的信息
    filename = argv[1];
    get_node_degree();
    get_link();
    //cout << node_degree.size() << endl;
    //cout << filename << endl;

    create_types(ofs);

    //by wyb
    int link_exist[2000] = {0};
    ofs << "\ttypes:\n";
    for (int i = 0; i < link.size(); ++i) {
        if(link_exist[link[i][2]] != 0)
            continue;
        link_exist[link[i][2]] = 1;
        //string Link = "LINK_" + link[i][2];
        string delay = "50us";
        //string datarate = link[i][2] + "Mbps";
        string displayAsTooltip = "true";
        string thruputDisplayFormat = "\"#N\"";
        ostringstream formatLink, formatDatarate;

        //21/6/24
        
        
        formatLink << "LINK_" << link[i][2];
        formatDatarate << link[i][2] << "Mbps";
        
        

        
        ofs << "\t\tchannel " << formatLink.str()<< " extends ThruputMeteringChannel\n";
        ofs << "\t\t{\n";
        ofs << "\t\t\tparameters:\n";
        ofs << "\t\t\t\tdelay = " << delay << ";\n";
        ofs << "\t\t\t\tdatarate = " << formatDatarate.str() << ";\n";
        ofs << "\t\t\t\tdisplayAsTooltip = " << displayAsTooltip << ";\n";
        ofs << "\t\t\t\tthruputDisplayFormat = " << thruputDisplayFormat << ";\n";
        ofs << "\t\t}" << endl;


    }

    create_submodules(ofs);
    create_connections(ofs);
    ofs << "}" << endl;
}
