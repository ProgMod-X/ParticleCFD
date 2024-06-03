using System.Collections.Generic;
using UnityEngine;

public class Simulation : MonoBehaviour
{
    public Mesh ParticleMesh;
    public Material ParticleMaterial;
    private List<Particle> particles = new List<Particle>();

    public Vector2 boundsSize;

    public float interactionRadius;

    void Start()
    {
        // Example: Create some particles
        for (int i = 0; i < 5; i++)
        {
            Vector3 position = new Vector3(Random.Range(-5, 5), Random.Range(-5, 5), 0);
            Vector3 velocity = new Vector3(Random.Range(-1, 1), Random.Range(-1, 1), 0);
            Color color = new Color(Random.value * 255, Random.value * 255, Random.value * 255);

            Particle particle = new Particle(position, velocity, color, ParticleMesh, ParticleMaterial);
            particles.Add(particle);
        }
    }

    void Update()
    {
        float deltaTime = Time.deltaTime;

        foreach (Particle particle in particles)
        {
            particle.Update(deltaTime);
        }
    }

    void OnRenderObject()
    {
        foreach (Particle particle in particles)
        {
            ParticleMaterial.color = particle.Color;
            ParticleMaterial.SetPass(0);
            Graphics.DrawMeshNow(particle.Mesh, particle.Position, Quaternion.identity);
        }
    }

    void OnDrawGizmos()
    {
        Gizmos.color = new Color(0, 1, 0, 0.4f);
        Gizmos.DrawWireCube(Vector2.zero, boundsSize);

        if (Application.isPlaying)
        {
            Vector2 mousePos = Camera.main.ScreenToWorldPoint(Input.mousePosition);
            bool isPullInteraction = Input.GetMouseButton(0);
            bool isPushInteraction = Input.GetMouseButton(1);
            bool isInteracting = isPullInteraction || isPushInteraction;
            if (isInteracting)
            {
                Gizmos.color = isPullInteraction ? Color.green : Color.red;
                Gizmos.DrawWireSphere(mousePos, interactionRadius);
            }
        }
    }
}
