from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, VPC, PublicSubnet, PrivateSubnet
from diagrams.aws.storage import S3

# Configuración del diagrama
# show=False evita que se intente abrir la imagen automáticamente (útil en servidores/CLI)
with Diagram("Basic Web Architecture AWS", show=False, direction="LR"):
    
    dns = ELB("DNS / Route53")
    
    with Cluster("VPC"):
        with Cluster("Public Subnet"):
            lb = ELB("Load Balancer")
        
        with Cluster("Private Subnet"):
            with Cluster("App Tier"):
                app_cluster = [EC2("Web Server 1"),
                               EC2("Web Server 2")]
            
            with Cluster("Database Tier"):
                db_master = RDS("User DB (Master)")
                db_master - Edge(color="brown", style="dotted") - RDS("User DB (Read Replica)")

    assets = S3("Static Assets")

    # Relaciones
    dns >> lb >> app_cluster
    app_cluster >> db_master
    app_cluster >> assets

print("Diagrama generado: basic_web_architecture_aws.png")
