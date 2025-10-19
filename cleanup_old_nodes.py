#!/usr/bin/env python3
import json
from datetime import datetime, timedelta

def cleanup_old_nodes():
    try:
        # Carica registry
        with open('nodes_registry.json', 'r') as f:
            registry = json.load(f)
        
        print(f"🔍 Nodi prima del cleanup: {len(registry['nodes'])}")
        
        # Calcola threshold (2 ore fa)
        threshold = datetime.now() - timedelta(hours=2)
        
        # Filtra nodi attivi
        active_nodes = []
        for node in registry['nodes']:
            try:
                last_seen = datetime.strptime(node['last_seen'], "%Y-%m-%d %H:%M:%S")
                if last_seen > threshold:
                    active_nodes.append(node)
                else:
                    print(f"🗑️ Rimuovo nodo inattivo: {node['address']}")
            except Exception as e:
                print(f"❌ Errore processo nodo {node['address']}: {e}")
                continue
        
        # Aggiorna registry
        registry['nodes'] = active_nodes
        registry['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Salva
        with open('nodes_registry.json', 'w') as f:
            json.dump(registry, f, indent=2)
        
        print(f"✅ Cleanup completato: {len(active_nodes)} nodi attivi")
        
    except Exception as e:
        print(f"💥 Errore durante cleanup: {e}")

if __name__ == "__main__":
    cleanup_old_nodes()
